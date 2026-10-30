"""Permission helpers for the core application."""
from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """Allow access only to admin users."""

    def has_permission(self, request, view) -> bool:  # type: ignore[override]
        return bool(request.user and request.user.is_staff)
