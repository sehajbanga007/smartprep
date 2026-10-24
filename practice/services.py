import html
import random

import requests
from django.conf import settings
from django.db.models import Avg, Count, Q

from . import question_bank
from .models import COMPLETED, PracticeAttempt
from .exceptions import ExternalAPIError, InsufficientQuestionsError, InvalidSubmissionError

MIN_AMOUNT = 3
MAX_AMOUNT = 7
DEFAULT_PLAYER_NAME = "Anonymous"


# ---------- local question bank logic ----------
def list_topics():
    return list(question_bank.TOPICS)


def select_questions(topic, difficulty, amount, rng=None):
    pool = [
        q for q in question_bank.QUESTIONS
        if q["topic"] == topic and q["difficulty"] == difficulty
    ]
    if len(pool) < amount:
        raise InsufficientQuestionsError(len(pool))
    return (rng or random).sample(pool, amount)


def public_question(question):
    """Question view that never contains the answer or explanation."""
    return {
        "id": question["id"],
        "topic": question["topic"],
        "difficulty": question["difficulty"],
        "question": question["question"],
        "options": question["options"],
    }


def calculate_percentage(correct, total):
    if correct < 0 or total < 0 or correct > total:
        raise ValueError("Invalid score values.")
    if total == 0:
        return 0.0
    return round(correct / total * 100, 2)


def grade_answers(snapshot, answers):
    """Score on the server. Unanswered questions count as incorrect."""
    by_id = {q["id"]: q for q in snapshot}
    given = {}
    for item in answers:
        qid = item["question_id"]
        if qid not in by_id:
            raise InvalidSubmissionError(f"Question {qid} does not belong to this attempt.")
        if qid in given:
            raise InvalidSubmissionError(f"Question {qid} was answered more than once.")
        given[qid] = item["selected_answer"]

    details, correct = [], 0
    for q in snapshot:
        selected = given.get(q["id"])
        is_correct = selected == q["correct_answer"]
        correct += is_correct
        details.append(
            {
                "question_id": q["id"],
                "selected_answer": selected,
                "correct_answer": q["correct_answer"],
                "is_correct": is_correct,
                "explanation": q["explanation"],
            }
        )
    total = len(snapshot)
    return {
        "total_questions": total,
        "answered_questions": len(given),
        "correct_answers": correct,
        "incorrect_answers": total - correct,
        "percentage": calculate_percentage(correct, total),
        "details": details,
    }


# ---------- leaderboard and stats ----------
# Ranking rule: higher percentage first; on a tie, the faster time wins;
# on a further tie, whoever finished first wins.
LEADERBOARD_ORDER = ("-percentage", "time_taken_seconds", "completed_at")


def clean_player_name(name):
    name = " ".join((name or "").split())
    return name or DEFAULT_PLAYER_NAME


def time_taken(started, finished):
    """Seconds between start and finish, rounded to 0.1 s (never negative)."""
    return max(0.0, round((finished - started).total_seconds(), 1))


def leaderboard(topic=None, difficulty=None, limit=10):
    rows = PracticeAttempt.objects.filter(status=COMPLETED)
    if topic:
        rows = rows.filter(topic=topic)
    if difficulty:
        rows = rows.filter(difficulty=difficulty)
    rows = rows.order_by(*LEADERBOARD_ORDER)[:limit]
    return [
        {
            "rank": position,
            "player_name": row.player_name,
            "topic": row.topic,
            "difficulty": row.difficulty,
            "total_questions": row.total_questions,
            "correct_answers": row.correct_count,
            "percentage": row.percentage,
            "time_taken_seconds": row.time_taken_seconds,
            "completed_at": row.completed_at.isoformat(),
        }
        for position, row in enumerate(rows, start=1)
    ]


def rank_of(attempt):
    """Position of a completed attempt among all attempts with the same topic and difficulty."""
    better = PracticeAttempt.objects.filter(
        status=COMPLETED, topic=attempt.topic, difficulty=attempt.difficulty
    ).filter(
        Q(percentage__gt=attempt.percentage)
        | Q(percentage=attempt.percentage, time_taken_seconds__lt=attempt.time_taken_seconds)
        | Q(
            percentage=attempt.percentage,
            time_taken_seconds=attempt.time_taken_seconds,
            completed_at__lt=attempt.completed_at,
        )
    )
    total = PracticeAttempt.objects.filter(
        status=COMPLETED, topic=attempt.topic, difficulty=attempt.difficulty
    ).count()
    return better.count() + 1, total


def stats():
    done = PracticeAttempt.objects.filter(status=COMPLETED)
    summary = done.aggregate(quizzes=Count("id"), average=Avg("percentage"))
    per_topic = (
        done.values("topic").annotate(quizzes=Count("id"), average=Avg("percentage")).order_by("-quizzes", "topic")
    )
    return {
        "completed_quizzes": summary["quizzes"],
        "players": done.values("player_name").distinct().count(),
        "average_percentage": round(summary["average"], 2) if summary["average"] is not None else None,
        "questions_in_bank": len(question_bank.QUESTIONS),
        "by_topic": [
            {"topic": r["topic"], "quizzes": r["quizzes"], "average_percentage": round(r["average"], 2)}
            for r in per_topic
        ],
    }


# ---------- Open Trivia DB ----------
def fetch_trivia_questions(amount):
    try:
        response = requests.get(
            settings.OPEN_TRIVIA_URL,
            params={"amount": amount, "type": "multiple"},
            timeout=settings.OPEN_TRIVIA_TIMEOUT,
        )
    except requests.Timeout:
        raise ExternalAPIError("external_timeout", "The trivia service timed out.", 504)
    except requests.RequestException:
        raise ExternalAPIError("external_unavailable", "The trivia service is unavailable.", 502)

    if response.status_code == 429:
        raise ExternalAPIError("external_rate_limited", "The trivia service is rate limiting requests.", 429)
    if response.status_code != 200:
        raise ExternalAPIError("external_http_error", "The trivia service returned an error.", 502)

    try:
        payload = response.json()
    except ValueError:
        raise ExternalAPIError("external_invalid_response", "The trivia service sent invalid data.", 502)
    return _normalize_trivia(payload)


def _normalize_trivia(payload):
    invalid = ExternalAPIError("external_invalid_response", "The trivia service sent unexpected data.", 502)
    if not isinstance(payload, dict) or not isinstance(payload.get("response_code"), int):
        raise invalid
    code = payload["response_code"]
    if code == 5:
        raise ExternalAPIError("external_rate_limited", "The trivia service is rate limiting requests.", 429)
    if code != 0:
        raise ExternalAPIError("external_no_results", "The trivia service could not return questions.", 502)
    results = payload.get("results")
    if not isinstance(results, list):
        raise invalid

    questions = []
    for item in results:
        try:
            correct = html.unescape(item["correct_answer"])
            options = [html.unescape(x) for x in item["incorrect_answers"]] + [correct]
            question = {
                "category": html.unescape(item["category"]),
                "difficulty": item["difficulty"],
                "question": html.unescape(item["question"]),
            }
        except (KeyError, TypeError, AttributeError):
            raise invalid
        random.shuffle(options)
        question.update({"options": options, "correct_answer": correct})
        questions.append(question)
    return questions
