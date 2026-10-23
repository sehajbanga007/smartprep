from rest_framework import serializers

from .question_bank import DIFFICULTIES, LETTERS, TOPICS
from .services import MAX_AMOUNT, MIN_AMOUNT


class PracticeSetCreateSerializer(serializers.Serializer):
    topic = serializers.ChoiceField(choices=TOPICS)
    difficulty = serializers.ChoiceField(choices=DIFFICULTIES)
    amount = serializers.IntegerField(min_value=MIN_AMOUNT, max_value=MAX_AMOUNT)


class AnswerItemSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected_answer = serializers.ChoiceField(choices=list(LETTERS))


class SubmitSerializer(serializers.Serializer):
    answers = AnswerItemSerializer(many=True, allow_empty=True)
