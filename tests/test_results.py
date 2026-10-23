import pytest

from practice.models import PracticeAttempt

pytestmark = [pytest.mark.api, pytest.mark.django_db]


def submit(api_client, attempt_id, answers):
    return api_client.post(f"/api/practice-sets/{attempt_id}/submit/", {"answers": answers}, format="json")


def test_all_correct_gives_100_percent_with_explanations(api_client, make_attempt, build_answers):
    attempt = make_attempt()
    response = submit(api_client, attempt["attempt_id"], build_answers(attempt["question_ids"], True))
    body = response.json()
    assert response.status_code == 200
    assert (body["total_questions"], body["answered_questions"]) == (3, 3)
    assert (body["correct_answers"], body["incorrect_answers"], body["percentage"]) == (3, 0, 100.0)
    assert all(d["explanation"] for d in body["details"])


def test_all_wrong_gives_zero(api_client, make_attempt, build_answers):
    attempt = make_attempt()
    body = submit(api_client, attempt["attempt_id"], build_answers(attempt["question_ids"], False)).json()
    assert body["correct_answers"] == 0 and body["percentage"] == 0.0


def test_mixed_answers_and_missing_answer(api_client, make_attempt, build_answers):
    attempt = make_attempt()
    ids = attempt["question_ids"]
    answers = build_answers(ids[:1], True) + build_answers(ids[1:2], False)  # third left unanswered
    body = submit(api_client, attempt["attempt_id"], answers).json()
    assert body["answered_questions"] == 2
    assert body["correct_answers"] == 1 and body["incorrect_answers"] == 2
    assert body["percentage"] == 33.33


def test_client_cannot_supply_score_or_correct_answer(api_client, make_attempt, build_answers):
    attempt = make_attempt()
    answers = build_answers(attempt["question_ids"], False)
    payload = {"answers": answers, "score": 100, "correct_answers": 3}
    body = api_client.post(f"/api/practice-sets/{attempt['attempt_id']}/submit/", payload, format="json").json()
    assert body["correct_answers"] == 0


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"answers": "A"},
        {"answers": ["A"]},
        {"answers": [{"question_id": 1}]},
        {"answers": [{"selected_answer": "A"}]},
        {"answers": [{"question_id": "x", "selected_answer": "A"}]},
        {"answers": [{"question_id": 1, "selected_answer": "E"}]},
    ],
)
def test_malformed_answer_structures(api_client, make_attempt, payload):
    attempt = make_attempt()
    response = api_client.post(f"/api/practice-sets/{attempt['attempt_id']}/submit/", payload, format="json")
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "validation_error"


def test_unknown_attempt_submit(api_client):
    response = submit(api_client, "00000000-0000-0000-0000-000000000000", [])
    assert response.status_code == 404 and response.json()["error"]["code"] == "attempt_not_found"


def test_question_from_another_attempt_is_rejected(api_client, make_attempt):
    mine = make_attempt("Django", "easy", 3)
    other = make_attempt("Docker", "easy", 3)
    foreign = other["question_ids"][0]
    response = submit(api_client, mine["attempt_id"], [{"question_id": foreign, "selected_answer": "A"}])
    assert response.status_code == 400 and response.json()["error"]["code"] == "invalid_submission"
    assert PracticeAttempt.objects.get(pk=mine["attempt_id"]).status == "in_progress"


def test_duplicate_question_in_one_submission_rejected(api_client, make_attempt):
    attempt = make_attempt()
    qid = attempt["question_ids"][0]
    answers = [{"question_id": qid, "selected_answer": "A"}] * 2
    assert submit(api_client, attempt["attempt_id"], answers).status_code == 400


def test_empty_answers_allowed_and_scores_zero(api_client, make_attempt):
    attempt = make_attempt()
    body = submit(api_client, attempt["attempt_id"], []).json()
    assert body["answered_questions"] == 0 and body["percentage"] == 0.0


def test_repeated_submission_is_rejected_and_result_unchanged(api_client, make_attempt, build_answers):
    attempt = make_attempt()
    ids = attempt["question_ids"]
    submit(api_client, attempt["attempt_id"], build_answers(ids, True))
    second = submit(api_client, attempt["attempt_id"], build_answers(ids, False))
    assert second.status_code == 409 and second.json()["error"]["code"] == "already_submitted"
    saved = api_client.get(f"/api/results/{attempt['attempt_id']}/").json()
    assert saved["percentage"] == 100.0


def test_result_is_persisted_in_database(api_client, make_attempt, build_answers):
    attempt = make_attempt()
    submit(api_client, attempt["attempt_id"], build_answers(attempt["question_ids"][:2], True))
    row = PracticeAttempt.objects.get(pk=attempt["attempt_id"])
    assert row.status == "completed" and row.completed_at is not None
    assert (row.correct_count, row.answered_count, row.percentage) == (2, 2, 66.67)


def test_get_results_for_completed_attempt(api_client, make_attempt, build_answers):
    attempt = make_attempt()
    submit(api_client, attempt["attempt_id"], build_answers(attempt["question_ids"], True))
    body = api_client.get(f"/api/results/{attempt['attempt_id']}/").json()
    assert body["status"] == "completed" and body["completed_at"]


def test_results_for_incomplete_and_unknown_attempts(api_client, make_attempt):
    attempt = make_attempt()
    incomplete = api_client.get(f"/api/results/{attempt['attempt_id']}/")
    assert incomplete.status_code == 409 and incomplete.json()["error"]["code"] == "attempt_not_completed"
    unknown = api_client.get("/api/results/00000000-0000-0000-0000-000000000000/")
    assert unknown.status_code == 404 and unknown.json()["error"]["code"] == "attempt_not_found"


def test_retrieval_after_submission_still_hides_answers(api_client, make_attempt, build_answers):
    attempt = make_attempt()
    submit(api_client, attempt["attempt_id"], build_answers(attempt["question_ids"], True))
    text = str(api_client.get(f"/api/practice-sets/{attempt['attempt_id']}/").json())
    assert "correct_answer" not in text and "explanation" not in text
