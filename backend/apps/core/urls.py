"""URL routes for the core application."""
from django.urls import path

from apps.core.views import HealthView, ReadinessView

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
    path("ready/", ReadinessView.as_view(), name="ready"),
]
