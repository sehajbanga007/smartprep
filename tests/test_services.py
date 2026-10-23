import random

import pytest
import requests
from django.conf import settings

from practice import question_bank, services
from practice.exceptions import ExternalAPIError, InsufficientQuestionsError, InvalidSubmissionError

pytestmark = pytest.mark.unit


# ---------- question selection and formatting ----------
def test_select_questions_matches_topic_and_difficulty():
    qs = services.select_questions("Django", "easy", 3)
    assert len(qs) == 3
    assert all(q["topic"] == "Django" and q["difficulty"] == "easy" for q in qs)


def test_select_questions_is_repeatable_with_seeded_rng():
    first = services.select_questions("HTML", "medium", 2, rng=random.Random(7))
    second = services.select_questions("HTML", "medium", 2, rng=random.Random(7))
    assert [q["id"] for q in first] == [q["id"] for q in second]


def test_select_questions_raises_when_not_enough():
    with pytest.raises(InsufficientQuestionsError) as info:
        services.select_questions("Docker", "hard", 10)
    assert info.value.available == 2


def test_list_topics_returns_copy_of_seven_topics():
    topics = services.list_topics()
    assert len(topics) == 7
    topics.append("X")
    assert len(services.list_topics()) == 7


def test_public_question_never_leaks_answer(sample_questions):
    public = services.public_question(sample_questions[0])
    assert set(public) == {"id", "topic", "difficulty", "question", "options"}
    assert "correct_answer" not in public and "explanation" not in public


# ---------- scoring ----------
def test_all_correct(sample_questions):
    answers = [{"question_id": 101, "selected_answer": "A"},
               {"question_id": 102, "selected_answer": "B"},
               {"question_id": 103, "selected_answer": "C"}]
    result = services.grade_answers(sample_questions, answers)
    assert result["correct_answers"] == 3 and result["incorrect_answers"] == 0
    assert result["percentage"] == 100.0


def test_all_incorrect(sample_questions):
    answers = [{"question_id": q["id"], "selected_answer": "D"} for q in sample_questions]
    result = services.grade_answers(sample_questions, answers)
    assert result["correct_answers"] == 0 and result["percentage"] == 0.0


def test_mixed_and_missing_answers_count_as_incorrect(sample_questions):
    answers = [{"question_id": 101, "selected_answer": "A"},
               {"question_id": 102, "selected_answer": "D"}]
    result = services.grade_answers(sample_questions, answers)
    assert result["answered_questions"] == 2
    assert result["correct_answers"] == 1
    assert result["incorrect_answers"] == 2
    assert result["percentage"] == 33.33
    by_id = {d["question_id"]: d for d in result["details"]}
    assert by_id[103]["selected_answer"] is None and by_id[103]["is_correct"] is False
    assert by_id[101]["explanation"] == "Because 101."


def test_empty_answers_scores_zero(sample_questions):
    result = services.grade_answers(sample_questions, [])
    assert result["answered_questions"] == 0 and result["percentage"] == 0.0


def test_foreign_question_id_rejected(sample_questions):
    with pytest.raises(InvalidSubmissionError):
        services.grade_answers(sample_questions, [{"question_id": 5, "selected_answer": "A"}])


def test_duplicate_question_in_submission_rejected(sample_questions):
    dup = [{"question_id": 101, "selected_answer": "A"}] * 2
    with pytest.raises(InvalidSubmissionError):
        services.grade_answers(sample_questions, dup)


@pytest.mark.parametrize(
    "correct,total,expected",
    [(0, 0, 0.0), (0, 5, 0.0), (5, 5, 100.0), (1, 3, 33.33), (2, 3, 66.67)],
)
def test_calculate_percentage(correct, total, expected):
    assert services.calculate_percentage(correct, total) == expected


@pytest.mark.parametrize("correct,total", [(-1, 3), (4, 3), (1, -3)])
def test_calculate_percentage_rejects_invalid_values(correct, total):
    with pytest.raises(ValueError):
        services.calculate_percentage(correct, total)


# ---------- Open Trivia DB service (mock the HTTP call: requests.get) ----------
def test_fetch_success_decodes_html_and_normalizes(monkeypatch, fake_response, trivia_payload):
    calls = []

    def fake_get(url, params=None, timeout=None):
        calls.append((url, params, timeout))
        return fake_response(200, trivia_payload)

    monkeypatch.setattr(services.requests, "get", fake_get)
    questions = services.fetch_trivia_questions(3)

    assert calls == [(settings.OPEN_TRIVIA_URL, {"amount": 3, "type": "multiple"}, settings.OPEN_TRIVIA_TIMEOUT)]
    q = questions[0]
    assert q["question"] == 'Fish & chips is served with "peas"?'
    assert q["correct_answer"] == "Mushy & green"
    assert sorted(q["options"]) == sorted(["Mushy & green", "Blue", "Red", "Purple"])
    assert "&amp;" not in str(q) and "&quot;" not in str(q)


def _expect_error(monkeypatch, getter, code, status):
    monkeypatch.setattr(services.requests, "get", getter)
    with pytest.raises(ExternalAPIError) as info:
        services.fetch_trivia_questions(3)
    assert info.value.code == code and info.value.status_code == status


def test_timeout(monkeypatch):
    def boom(*a, **k):
        raise requests.Timeout("secret internal detail")

    _expect_error(monkeypatch, boom, "external_timeout", 504)


def test_connection_failure_hides_internal_details(monkeypatch):
    def boom(*a, **k):
        raise requests.ConnectionError("secret internal detail")

    monkeypatch.setattr(services.requests, "get", boom)
    with pytest.raises(ExternalAPIError) as info:
        services.fetch_trivia_questions(3)
    assert info.value.code == "external_unavailable"
    assert "secret" not in info.value.message


def test_http_500(monkeypatch, fake_response):
    _expect_error(monkeypatch, lambda *a, **k: fake_response(500), "external_http_error", 502)


def test_http_429(monkeypatch, fake_response):
    _expect_error(monkeypatch, lambda *a, **k: fake_response(429), "external_rate_limited", 429)


def test_malformed_json(monkeypatch, fake_response):
    _expect_error(monkeypatch, lambda *a, **k: fake_response(200, bad_json=True), "external_invalid_response", 502)


@pytest.mark.parametrize("code,expected_code,status", [(5, "external_rate_limited", 429), (1, "external_no_results", 502), (2, "external_no_results", 502)])
def test_open_trivia_response_codes(monkeypatch, fake_response, code, expected_code, status):
    payload = {"response_code": code, "results": []}
    _expect_error(monkeypatch, lambda *a, **k: fake_response(200, payload), expected_code, status)


@pytest.mark.parametrize(
    "payload",
    [
        [],
        {"results": []},
        {"response_code": "0", "results": []},
        {"response_code": 0},
        {"response_code": 0, "results": "nope"},
        {"response_code": 0, "results": [{"question": "only this"}]},
        {"response_code": 0, "results": [None]},
    ],
)
def test_unexpected_payload_structures(monkeypatch, fake_response, payload):
    _expect_error(monkeypatch, lambda *a, **k: fake_response(200, payload), "external_invalid_response", 502)
