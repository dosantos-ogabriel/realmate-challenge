from rest_framework import serializers
from .models import Conversation
from .choices import MessageDirection, ConversationState


class WebhookSerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        choices=[
            "NEW_CONVERSATION",
            "NEW_MESSAGE",
            "CLOSE_CONVERSATION",
        ]
    )
    timestamp = serializers.DateTimeField()
    data = serializers.JSONField()

    def validate(self, data):
        type_serializers = {
            "NEW_CONVERSATION": NewConversationSerializer,
            "NEW_MESSAGE": NewMessageSerializer,
            "CLOSE_CONVERSATION": CloseConversationSerializer,
        }
        serializer_type = type_serializers[data["type"]]
        serializer = serializer_type(data=data["data"])
        serializer.is_valid(raise_exception=True)

        data["data"] = serializer.validated_data
        return data


class NewConversationSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class CloseConversationSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class NewMessageSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    conversation_id = serializers.UUIDField()
    content = serializers.CharField()
    direction = serializers.ChoiceField(choices=MessageDirection.choices)
