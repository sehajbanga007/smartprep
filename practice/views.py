import uuid

from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from . import services
from .exceptions import ExternalAPIError, InsufficientQuestionsError, InvalidSubmissionError
from .models import COMPLETED, IN_PROGRESS, PracticeAttempt
from .serializers import LeaderboardQuerySerializer, PracticeSetCreateSerializer, SubmitSerializer
from .services import fetch_trivia_questions


def error_response(code, message, status_code, details=None):
    body = {"error": {"code": code, "message": message}}
    if details is not None:
        body["error"]["details"] = details
    return Response(body, status=status_code)


def _find_attempt(attempt_id):
    try:
        key = uuid.UUID(str(attempt_id))
    except ValueError:
        return None
    return PracticeAttempt.objects.filter(pk=key).first()


def _not_found():
    return error_response("attempt_not_found", "Practice attempt not found.", 404)


def _attempt_payload(attempt):
    return {
        "attempt_id": str(attempt.id),
        "player_name": attempt.player_name,
        "topic": attempt.topic,
        "difficulty": attempt.difficulty,
        "status": attempt.status,
        "started_at": attempt.created_at.isoformat(),
        "total_questions": attempt.total_questions,
        "question_ids": [q["id"] for q in attempt.questions],
        "questions": [services.public_question(q) for q in attempt.questions],
    }


def _result_payload(attempt):
    rank, ranked = services.rank_of(attempt)
    return {
        "attempt_id": str(attempt.id),
        "player_name": attempt.player_name,
        "topic": attempt.topic,
        "difficulty": attempt.difficulty,
        "status": attempt.status,
        "total_questions": attempt.total_questions,
        "answered_questions": attempt.answered_count,
        "correct_answers": attempt.correct_count,
        "incorrect_answers": attempt.total_questions - attempt.correct_count,
        "percentage": attempt.percentage,
        "completed_at": attempt.completed_at.isoformat() if attempt.completed_at else None,
        "time_taken_seconds": attempt.time_taken_seconds,
        "rank": rank,
        "ranked_attempts": ranked,
        "details": attempt.details,
    }


class HealthView(APIView):
    def get(self, request):
        return Response({"status": "ok"})


class TopicsView(APIView):
    def get(self, request):
        return Response({"topics": services.list_topics()})


class PracticeSetCreateView(APIView):
    def post(self, request):
        serializer = PracticeSetCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response("validation_error", "Invalid request.", 400, serializer.errors)
        data = serializer.validated_data
        try:
            questions = services.select_questions(data["topic"], data["difficulty"], data["amount"])
        except InsufficientQuestionsError as exc:
            return error_response(
                "insufficient_questions",
                f"Only {exc.available} {data['difficulty']} {data['topic']} questions are available.",
                422,
            )
        attempt = PracticeAttempt.objects.create(
            player_name=services.clean_player_name(data.get("player_name")),
            topic=data["topic"],
            difficulty=data["difficulty"],
            questions=questions,
            total_questions=len(questions),
        )
        return Response(_attempt_payload(attempt), status=201)


class PracticeSetDetailView(APIView):
    def get(self, request, attempt_id):
        attempt = _find_attempt(attempt_id)
        if attempt is None:
            return _not_found()
        return Response(_attempt_payload(attempt))


class SubmitView(APIView):
    def post(self, request, attempt_id):
        attempt = _find_attempt(attempt_id)
        if attempt is None:
            return _not_found()
        if attempt.status == COMPLETED:
            return error_response("already_submitted", "This attempt was already submitted.", 409)

        serializer = SubmitSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response("validation_error", "Invalid request.", 400, serializer.errors)
        try:
            result = services.grade_answers(attempt.questions, serializer.validated_data["answers"])
        except InvalidSubmissionError as exc:
            return error_response("invalid_submission", str(exc), 400)

        # Conditional update: only the first submission can win.
        now = timezone.now()
        updated = PracticeAttempt.objects.filter(pk=attempt.pk, status=IN_PROGRESS).update(
            status=COMPLETED,
            time_taken_seconds=services.time_taken(attempt.created_at, now),
            answered_count=result["answered_questions"],
            correct_count=result["correct_answers"],
            percentage=result["percentage"],
            details=result["details"],
            completed_at=now,
        )
        if not updated:
            return error_response("already_submitted", "This attempt was already submitted.", 409)
        attempt.refresh_from_db()
        return Response(_result_payload(attempt))


class ResultView(APIView):
    def get(self, request, attempt_id):
        attempt = _find_attempt(attempt_id)
        if attempt is None:
            return _not_found()
        if attempt.status != COMPLETED:
            return error_response("attempt_not_completed", "This attempt has not been submitted yet.", 409)
        return Response(_result_payload(attempt))


class LeaderboardView(APIView):
    def get(self, request):
        query = LeaderboardQuerySerializer(data=request.query_params)
        if not query.is_valid():
            return error_response("validation_error", "Invalid leaderboard filter.", 400, query.errors)
        data = query.validated_data
        return Response(
            {
                "topic": data.get("topic"),
                "difficulty": data.get("difficulty"),
                "ranking": "Highest percentage first; ties go to the faster time.",
                "entries": services.leaderboard(data.get("topic"), data.get("difficulty"), data["limit"]),
            }
        )


class StatsView(APIView):
    def get(self, request):
        return Response(services.stats())


class ExternalTriviaView(APIView):
    def get(self, request):
        raw = request.query_params.get("amount", "5")
        try:
            amount = int(raw)
        except ValueError:
            return error_response("validation_error", "amount must be an integer.", 400)
        if not 1 <= amount <= 20:
            return error_response("validation_error", "amount must be between 1 and 20.", 400)
        try:
            questions = fetch_trivia_questions(amount)
        except ExternalAPIError as exc:
            return error_response(exc.code, exc.message, exc.status_code)
        return Response({"source": "Open Trivia DB", "count": len(questions), "questions": questions})
