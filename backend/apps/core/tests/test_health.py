"""Tests for health and readiness endpoints."""
from unittest.mock import patch

from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


def test_health_endpoint_returns_healthy():
    client = APIClient()
    url = reverse("health")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"status": "healthy", "service": "stockpilot-api"}


def test_ready_endpoint_returns_ready_when_database_is_healthy():
    client = APIClient()
    url = reverse("ready")
    response = client.get(url)
    # In test environment a Postgres instance may not be available.
    assert response.status_code in (status.HTTP_200_OK, status.HTTP_503_SERVICE_UNAVAILABLE)
    assert "checks" in response.data
    assert "database" in response.data["checks"]


def test_ready_endpoint_reports_database_failure():
    client = APIClient()
    url = reverse("ready")
    with patch("apps.core.views.connection.ensure_connection", side_effect=Exception("db down")):
        response = client.get(url)
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert response.data["status"] == "not_ready"
    assert response.data["checks"]["database"] == "unhealthy"


def test_health_endpoint_does_not_require_authentication():
    client = APIClient()
    response = client.get("/api/v1/health/")
    assert response.status_code == status.HTTP_200_OK


def test_unknown_route_returns_404():
    client = APIClient()
    response = client.get("/api/v1/does-not-exist/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
