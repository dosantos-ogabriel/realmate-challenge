from django.urls import path

from .views import WebhookApiView, ConversationViewSet

urlpatterns = [
    path(
        "webhook/",
        WebhookApiView.as_view(),
        name="webhook",
    ),
    path(
        "conversations/<str:pk>",
        ConversationViewSet.as_view({"get": "retrieve"}),
        name="conversation",
    ),
]
