from datetime import timedelta

import pytest

from practice import services
from practice.models import PracticeAttempt

pytestmark = [pytest.mark.api, pytest.mark.django_db]


@pytest.fixture
def play(api_client, build_answers):
    """Create and submit an attempt that took `seconds` and got `correct` of 3 right."""

    def _play(name, correct=3, seconds=30, topic="HTML", difficulty="easy"):
        created = api_client.post(
            "/api/practice-sets/",
            {"player_name": name, "topic": topic, "difficulty": difficulty, "amount": 3},
            format="json",
        ).json()
        ids = created["question_ids"]
        # Pretend the attempt started `seconds` ago, so time taken is predictable.
        started = PracticeAttempt.objects.get(pk=created["attempt_id"]).created_at - timedelta(seconds=seconds)
        PracticeAttempt.objects.filter(pk=created["attempt_id"]).update(created_at=started)
        answers = build_answers(ids[:correct], True) + build_answers(ids[correct:], False)
        response = api_client.post(f"/api/practice-sets/{created['attempt_id']}/submit/", {"answers": answers}, format="json")
        assert response.status_code == 200
        return response.json()

    return _play


def board(api_client, query=""):
    response = api_client.get(f"/api/leaderboard/{query}")
    assert response.status_code == 200
    return response.json()["entries"]


def test_player_name_is_saved_and_returned(api_client):
    body = api_client.post(
        "/api/practice-sets/", {"player_name": "  Sehaj   B ", "topic": "CSS", "difficulty": "easy", "amount": 3}, format="json"
    ).json()
    assert body["player_name"] == "Sehaj B"
    assert body["started_at"]


@pytest.mark.parametrize("name", [None, "", "   "])
def test_missing_or_blank_name_becomes_anonymous(api_client, name):
    payload = {"topic": "CSS", "difficulty": "easy", "amount": 3}
    if name is not None:
        payload["player_name"] = name
    assert api_client.post("/api/practice-sets/", payload, format="json").json()["player_name"] == "Anonymous"


def test_time_taken_is_measured_on_the_server(play):
    result = play("Asha", seconds=42)
    assert 42 <= result["time_taken_seconds"] < 45


def test_client_cannot_send_its_own_time(api_client, make_attempt, build_answers):
    attempt = make_attempt()
    row = PracticeAttempt.objects.get(pk=attempt["attempt_id"])
    PracticeAttempt.objects.filter(pk=row.pk).update(created_at=row.created_at - timedelta(seconds=30))
    payload = {"answers": build_answers(attempt["question_ids"], True), "time_taken_seconds": 0.1}
    body = api_client.post(f"/api/practice-sets/{attempt['attempt_id']}/submit/", payload, format="json").json()
    assert body["time_taken_seconds"] >= 30


def test_leaderboard_orders_by_score_then_time(api_client, play):
    play("Slow perfect", correct=3, seconds=90)
    play("Fast perfect", correct=3, seconds=20)
    play("Fast but wrong", correct=1, seconds=5)
    entries = board(api_client)
    assert [e["player_name"] for e in entries] == ["Fast perfect", "Slow perfect", "Fast but wrong"]
    assert [e["rank"] for e in entries] == [1, 2, 3]
    assert entries[0]["percentage"] == 100.0 and entries[0]["correct_answers"] == 3


def test_leaderboard_never_shows_answers_or_unfinished_attempts(api_client, play, make_attempt):
    play("Done")
    make_attempt()  # still in progress
    entries = board(api_client)
    assert len(entries) == 1
    for entry in entries:
        assert not {"correct_answer", "explanation", "details", "questions"} & set(entry)


def test_leaderboard_filters_and_limit(api_client, play):
    play("H1", topic="HTML")
    play("D1", topic="Docker")
    play("D2", topic="Docker", difficulty="hard")
    assert [e["player_name"] for e in board(api_client, "?topic=Docker")] in (["D1", "D2"], ["D2", "D1"])
    assert [e["player_name"] for e in board(api_client, "?topic=Docker&difficulty=hard")] == ["D2"]
    assert len(board(api_client, "?limit=1")) == 1


@pytest.mark.parametrize("query", ["?topic=IMAP", "?difficulty=extreme", "?limit=0", "?limit=51", "?limit=abc"])
def test_leaderboard_rejects_bad_filters(api_client, query):
    response = api_client.get(f"/api/leaderboard/{query}")
    assert response.status_code == 400 and response.json()["error"]["code"] == "validation_error"


def test_result_includes_rank_among_same_topic_and_difficulty(play):
    play("First", correct=3, seconds=10)
    play("Other topic", correct=3, seconds=1, topic="CSS")
    result = play("Second", correct=3, seconds=50)
    assert (result["rank"], result["ranked_attempts"]) == (2, 2)


def test_stats(api_client, play):
    assert api_client.get("/api/stats/").json()["completed_quizzes"] == 0
    play("A", correct=3)
    play("B", correct=0, topic="CSS")
    body = api_client.get("/api/stats/").json()
    assert body["completed_quizzes"] == 2 and body["players"] == 2
    assert body["average_percentage"] == 50.0
    assert body["questions_in_bank"] == 147
    assert {row["topic"] for row in body["by_topic"]} == {"HTML", "CSS"}


def test_time_taken_helper_never_negative():
    from django.utils import timezone

    now = timezone.now()
    assert services.time_taken(now, now - timedelta(seconds=5)) == 0.0
    assert services.time_taken(now, now + timedelta(seconds=12.34)) == 12.3
