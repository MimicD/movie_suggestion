from rest_framework import serializers
from .models import Prompt

class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = ["id", "text", "author", "date_created_at", "response"]
        extra_kwargs = {
            'author': {'read_only': True},
            'date_created_at': {'read_only': True},
            'response': {'read_only': True}
        }

    def validate_text(self, value):
        words = value.split()
        if len(words) < 3:
            raise serializers.ValidationError("Prompt should be contain at lest 3 words")
        return value