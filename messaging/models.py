from django.db import models
from .choices import MessageDirection, ConversationState


class ConversationState(models.TextChoices):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    state = models.CharField(
        max_length=10, choices=ConversationState.choices, default=ConversationState.OPEN
    )


class Message(models.Model):
    id = models.UUIDField(primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sent_at = models.DateTimeField()
    content = models.TextField()
    direction = models.CharField(max_length=10, choices=MessageDirection.choices)
