from django.db import models


class ConversationState(models.TextChoices):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class MessageDirection(models.TextChoices):
    SENT = "SENT"
    RECEIVED = "RECEIVED"
