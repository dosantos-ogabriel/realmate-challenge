from django.urls import path

from .views import WebhookApiView

urlpatterns = [
    path(
        "webhook/",
        WebhookApiView.as_view(),
        name="webhook",
    ),
]
