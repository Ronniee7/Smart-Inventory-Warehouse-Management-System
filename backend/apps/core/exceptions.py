"""API exception handling for StockPilot."""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def api_exception_handler(exc, context):
    """Wrap DRF's default handler with a consistent error envelope."""
    response = drf_exception_handler(exc, context)
    if response is None:
        return None
    if not isinstance(response.data, dict):
        response.data = {"detail": response.data}
    if "detail" in response.data and "code" not in response.data:
        response.data.setdefault("code", "error")
    if response.status_code >= 500:
        response.data = {
            "detail": "An internal server error occurred.",
            "code": "server_error",
        }
    return response
