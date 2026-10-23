import html
import random

import requests
from django.conf import settings

from . import question_bank
from .exceptions import ExternalAPIError, InsufficientQuestionsError, InvalidSubmissionError

MIN_AMOUNT = 1
MAX_AMOUNT = 10


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
