import pytest

from practice.exceptions import ExternalAPIError

pytestmark = [pytest.mark.api, pytest.mark.django_db]

FORBIDDEN_KEYS = ("correct_answer", "explanation")


def assert_error(response, status, code):
    assert response.status_code == status
    body = response.json()
    assert body["error"]["code"] == code
    assert body["error"]["message"]


def test_health(api_client):
    response = api_client.get("/api/health/")
    assert response.status_code == 200 and response.json() == {"status": "ok"}


def test_topics_are_exactly_the_seven_syllabus_topics(api_client):
    topics = api_client.get("/api/topics/").json()["topics"]
    assert topics == ["HTML", "CSS", "JavaScript", "MongoDB", "NoSQL", "Django", "Docker"]


def test_method_not_allowed_uses_error_format(api_client):
    assert_error(api_client.delete("/api/topics/"), 405, "method_not_allowed")


def test_create_practice_set(make_attempt):
    data = make_attempt("Django", "easy", 3)
    assert data["status"] == "in_progress"
    assert len(data["question_ids"]) == 3 == len(data["questions"])
    assert all(q["topic"] == "Django" and q["difficulty"] == "easy" for q in data["questions"])


def test_create_and_retrieve_never_leak_answers(api_client, make_attempt):
    created = make_attempt()
    retrieved = api_client.get(f"/api/practice-sets/{created['attempt_id']}/").json()
    for payload in (created, retrieved):
        text = str(payload)
        assert not any(key in text for key in FORBIDDEN_KEYS)
    assert retrieved["question_ids"] == created["question_ids"]


def test_retrieve_unknown_and_invalid_ids(api_client):
    assert_error(api_client.get("/api/practice-sets/00000000-0000-0000-0000-000000000000/"), 404, "attempt_not_found")
    assert_error(api_client.get("/api/practice-sets/not-a-uuid/"), 404, "attempt_not_found")


@pytest.mark.parametrize(
    "body",
    [
        {"topic": "IMAP", "difficulty": "easy", "amount": 3},
        {"topic": "Django", "difficulty": "extreme", "amount": 3},
        {"difficulty": "easy", "amount": 3},
        {"topic": "Django", "amount": 3},
        {"topic": "Django", "difficulty": "easy"},
        {"topic": "Django", "difficulty": "easy", "amount": 0},
        {"topic": "Django", "difficulty": "easy", "amount": 2},
        {"topic": "Django", "difficulty": "easy", "amount": 8},
        {"topic": "Django", "difficulty": "easy", "amount": 3, "player_name": "x" * 21},
        {"topic": "Django", "difficulty": "easy", "amount": 3, "player_name": "<script>"},
        {"topic": "Django", "difficulty": "easy", "amount": "many"},
        {},
    ],
)
def test_create_validation_errors(api_client, body):
    response = api_client.post("/api/practice-sets/", body, format="json")
    assert_error(response, 400, "validation_error")
    assert "details" in response.json()["error"]


def test_create_with_malformed_json(api_client):
    response = api_client.post("/api/practice-sets/", data="{bad json", content_type="application/json")
    assert_error(response, 400, "parse_error")


def test_create_with_non_object_json(api_client):
    assert_error(api_client.post("/api/practice-sets/", [1, 2], format="json"), 400, "validation_error")


@pytest.mark.parametrize("amount", [3, 4, 5, 6, 7])
def test_every_amount_from_3_to_7_works_for_every_difficulty(make_attempt, amount):
    for difficulty in ("easy", "medium", "hard"):
        data = make_attempt("Docker", difficulty, amount)
        assert len(data["questions"]) == amount


def test_insufficient_questions(api_client, monkeypatch):
    from practice.exceptions import InsufficientQuestionsError

    def short(*args, **kwargs):
        raise InsufficientQuestionsError(2)

    monkeypatch.setattr("practice.services.select_questions", short)
    response = api_client.post(
        "/api/practice-sets/", {"topic": "Django", "difficulty": "easy", "amount": 5}, format="json"
    )
    assert_error(response, 422, "insufficient_questions")


# ---------- external trivia: API tests mock the SERVICE function used by the view ----------
def test_external_trivia_success(api_client, monkeypatch):
    fake = [{"category": "GK", "difficulty": "easy", "question": "Q?", "options": ["a", "b"], "correct_answer": "a"}]
    monkeypatch.setattr("practice.views.fetch_trivia_questions", lambda amount: fake)
    body = api_client.get("/api/external-trivia/?amount=1").json()
    assert body["source"] == "Open Trivia DB" and body["count"] == 1


@pytest.mark.parametrize(
    "error,status",
    [
        (ExternalAPIError("external_timeout", "timed out", 504), 504),
        (ExternalAPIError("external_http_error", "bad", 502), 502),
        (ExternalAPIError("external_invalid_response", "malformed", 502), 502),
        (ExternalAPIError("external_rate_limited", "slow down", 429), 429),
    ],
)
def test_external_trivia_errors_are_safe(api_client, monkeypatch, error, status):
    def boom(amount):
        raise error

    monkeypatch.setattr("practice.views.fetch_trivia_questions", boom)
    assert_error(api_client.get("/api/external-trivia/"), status, error.code)


@pytest.mark.parametrize("amount", ["0", "21", "abc"])
def test_external_trivia_validates_amount(api_client, amount):
    assert_error(api_client.get(f"/api/external-trivia/?amount={amount}"), 400, "validation_error")


def test_external_trivia_end_to_end_with_mocked_http_timeout(api_client, monkeypatch):
    """View + real service code; only the HTTP call (requests.get) is mocked."""
    import requests

    def boom(*a, **k):
        raise requests.Timeout("slow")

    monkeypatch.setattr("practice.services.requests.get", boom)
    assert_error(api_client.get("/api/external-trivia/"), 504, "external_timeout")
