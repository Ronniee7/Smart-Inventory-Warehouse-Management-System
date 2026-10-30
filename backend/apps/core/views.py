"""Health and readiness views for StockPilot."""
from django.db import connection
from django.db.utils import OperationalError
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthView(APIView):
    """Liveness check: is the application process running?"""

    permission_classes = [AllowAny]
    authentication_classes: list = []

    def get(self, request):
        return Response(
            {"status": "healthy", "service": "stockpilot-api"},
            status=status.HTTP_200_OK,
        )


class ReadinessView(APIView):
    """Readiness check: are essential dependencies available?"""

    permission_classes = [AllowAny]
    authentication_classes: list = []

    def get(self, request):
        checks = {}
        overall = "ready"
        try:
            connection.ensure_connection()
            checks["database"] = "healthy"
        except OperationalError:
            checks["database"] = "unhealthy"
            overall = "not_ready"

        http_status = (
            status.HTTP_200_OK if overall == "ready" else status.HTTP_503_SERVICE_UNAVAILABLE
        )
        return Response(
            {"status": overall, "checks": checks},
            status=http_status,
        )
