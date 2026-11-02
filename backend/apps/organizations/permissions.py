"""Permission classes for organizations."""
from rest_framework import permissions

from apps.organizations.models import OrganizationMembership, Role


def get_membership(user, organization_id):
    if not user.is_authenticated:
        return None
    try:
        return OrganizationMembership.objects.get(
            user=user, organization_id=organization_id, is_active=True
        )
    except OrganizationMembership.DoesNotExist:
        return None


class IsOrganizationMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        membership = get_membership(request.user, obj.id if hasattr(obj, "id") else obj.pk)
        return membership is not None


class IsOrganizationAdmin(permissions.BasePermission):
    """Owner or Admin."""

    def has_object_permission(self, request, view, obj):
        membership = get_membership(request.user, obj.id if hasattr(obj, "id") else obj.pk)
        if membership is None:
            return False
        return membership.role in (Role.OWNER, Role.ADMIN)


class IsOrganizationOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        membership = get_membership(request.user, obj.id if hasattr(obj, "id") else obj.pk)
        if membership is None:
            return False
        return membership.role == Role.OWNER
