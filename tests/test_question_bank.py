import pytest

from practice import question_bank

pytestmark = pytest.mark.unit

SYLLABUS = ["HTML", "CSS", "JavaScript", "MongoDB", "NoSQL", "Django", "Docker"]


def test_exactly_seven_syllabus_topics_and_no_imap():
    assert question_bank.TOPICS == SYLLABUS
    assert "IMAP" not in question_bank.TOPICS


def test_bank_has_at_least_56_questions_with_unique_ids():
    ids = [q["id"] for q in question_bank.QUESTIONS]
    assert len(ids) >= 56
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize("topic", SYLLABUS)
def test_each_topic_has_at_least_eight_questions_in_every_difficulty_range(topic):
    qs = [q for q in question_bank.QUESTIONS if q["topic"] == topic]
    assert len(qs) >= 8
    assert {q["difficulty"] for q in qs} == {"easy", "medium", "hard"}


def test_every_question_is_well_formed():
    for q in question_bank.QUESTIONS:
        assert q["topic"] in SYLLABUS
        assert q["difficulty"] in question_bank.DIFFICULTIES
        assert q["question"].strip()
        assert list(q["options"]) == ["A", "B", "C", "D"]
        assert len(set(q["options"].values())) == 4
        assert q["correct_answer"] in q["options"]
        assert q["explanation"].strip()


def test_correct_letters_are_varied():
    assert len({q["correct_answer"] for q in question_bank.QUESTIONS}) == 4


def test_get_question_known_and_unknown():
    assert question_bank.get_question(1)["id"] == 1
    assert question_bank.get_question(99999) is None
