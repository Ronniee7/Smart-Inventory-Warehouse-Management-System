"""Tenant scoping helpers for organizations."""
from apps.organizations.models import Organization, OrganizationMembership


def user_organizations(user):
    return Organization.objects.filter(memberships__user=user, memberships__is_active=True).distinct()


def user_membership(user, organization_id):
    try:
        return OrganizationMembership.objects.get(
            user=user, organization_id=organization_id, is_active=True
        )
    except OrganizationMembership.DoesNotExist:
        return None


def is_member(user, organization_id):
    return user_membership(user, organization_id) is not None
