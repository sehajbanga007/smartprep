from rest_framework import serializers

from .question_bank import DIFFICULTIES, LETTERS, TOPICS
from .services import MAX_AMOUNT, MIN_AMOUNT


class PracticeSetCreateSerializer(serializers.Serializer):
    player_name = serializers.CharField(max_length=20, required=False, allow_blank=True, trim_whitespace=True)
    topic = serializers.ChoiceField(choices=TOPICS)
    difficulty = serializers.ChoiceField(choices=DIFFICULTIES)
    amount = serializers.IntegerField(min_value=MIN_AMOUNT, max_value=MAX_AMOUNT)

    def validate_player_name(self, value):
        value = " ".join(value.split())
        if any(ch in value for ch in "<>"):
            raise serializers.ValidationError("Name cannot contain < or >.")
        return value


class AnswerItemSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected_answer = serializers.ChoiceField(choices=list(LETTERS))


class SubmitSerializer(serializers.Serializer):
    answers = AnswerItemSerializer(many=True, allow_empty=True)


class LeaderboardQuerySerializer(serializers.Serializer):
    topic = serializers.ChoiceField(choices=TOPICS, required=False)
    difficulty = serializers.ChoiceField(choices=DIFFICULTIES, required=False)
    limit = serializers.IntegerField(min_value=1, max_value=50, required=False, default=10)
