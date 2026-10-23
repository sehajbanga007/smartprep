import pytest
import requests
from rest_framework.test import APIClient

from practice import question_bank


@pytest.fixture(autouse=True)
def block_live_http(monkeypatch):
    """Safety net: any un-mocked HTTP request fails the test instead of hitting the internet."""

    def _blocked(*args, **kwargs):
        raise AssertionError("Live HTTP request attempted in a test - mock it!")

    monkeypatch.setattr(requests.sessions.Session, "request", _blocked)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def sample_questions():
    def q(qid, correct):
        return {
            "id": qid, "topic": "Django", "difficulty": "easy", "question": f"Question {qid}?",
            "options": {"A": "a", "B": "b", "C": "c", "D": "d"},
            "correct_answer": correct, "explanation": f"Because {qid}.",
        }

    return [q(101, "A"), q(102, "B"), q(103, "C")]


@pytest.fixture
def make_attempt(api_client, db):
    """Create a practice set through the real API and return its JSON."""

    def _make(topic="Django", difficulty="easy", amount=3):
        response = api_client.post(
            "/api/practice-sets/",
            {"topic": topic, "difficulty": difficulty, "amount": amount},
            format="json",
        )
        assert response.status_code == 201
        return response.json()

    return _make


@pytest.fixture
def build_answers():
    """Build answer payloads: correct=True picks the right letter, False a wrong one."""

    def _build(question_ids, correct=True):
        answers = []
        for qid in question_ids:
            right = question_bank.get_question(qid)["correct_answer"]
            chosen = right if correct else next(x for x in "ABCD" if x != right)
            answers.append({"question_id": qid, "selected_answer": chosen})
        return answers

    return _build


@pytest.fixture
def trivia_payload():
    return {
        "response_code": 0,
        "results": [
            {
                "category": "General Knowledge",
                "type": "multiple",
                "difficulty": "easy",
                "question": "Fish &amp; chips is served with &quot;peas&quot;?",
                "correct_answer": "Mushy &amp; green",
                "incorrect_answers": ["Blue", "Red", "Purple"],
            }
        ],
    }


class FakeResponse:
    def __init__(self, status_code=200, payload=None, bad_json=False):
        self.status_code = status_code
        self._payload = payload
        self._bad_json = bad_json

    def json(self):
        if self._bad_json:
            raise ValueError("not json")
        return self._payload


@pytest.fixture
def fake_response():
    return FakeResponse
