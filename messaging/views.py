from rest_framework import views, status
from rest_framework.response import Response

from django.db.utils import IntegrityError

from .models import Conversation, Message
from .choices import ConversationState
from .serializers import WebhookSerializer


class WebhookApiView(views.APIView):
    serializer_class = WebhookSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        actions = {
            "NEW_CONVERSATION": self.create_conversation,
            "NEW_MESSAGE": self.create_message,
            "CLOSE_CONVERSATION": self.close_conversation,
        }
        return actions[data["type"]](data)

    def create_conversation(self, data):
        try:
            Conversation.objects.create(created_at=data["timestamp"], **data["data"])
        except IntegrityError:
            return Response(
                status=status.HTTP_409_CONFLICT,
                data={"message": "Conversation with this id already exists"},
            )
        return Response(
            {"message": "Conversation created"}, status=status.HTTP_201_CREATED
        )

    def close_conversation(self, data):
        conversation_id = data["data"]["id"]
        conversation = Conversation.objects.get(id=conversation_id)
        if conversation.state == ConversationState.CLOSED:
            return Response(
                status=status.HTTP_409_CONFLICT,
                data={"message": "Conversation is already closed"},
            )

        conversation.state = ConversationState.CLOSED
        conversation.closed_at = data["timestamp"]
        conversation.save()
        return Response(status=status.HTTP_200_OK)

    def create_message(self, data):
        try:
            conversation = Conversation.objects.get(id=data["data"]["conversation_id"])
        except Conversation.DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Conversation does not exist"},
            )

        if conversation.state == ConversationState.CLOSED:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Conversation is closed"},
            )

        try:
            Message.objects.create(sent_at=data["timestamp"], **data["data"])
        except IntegrityError:
            return Response(
                status=status.HTTP_409_CONFLICT,
                data={"message": "Message with this id already exists"},
            )
        return Response({"message": "Message sent"}, status=status.HTTP_201_CREATED)
