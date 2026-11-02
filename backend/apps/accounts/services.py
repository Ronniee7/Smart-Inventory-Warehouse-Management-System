"""Service functions for accounts."""
from django.contrib.auth import get_user_model
from django.db import transaction

from apps.organizations.models import Organization, OrganizationMembership, Role

User = get_user_model()


def register_user(*, email: str, password: str, username: str, organization_name: str):
    with transaction.atomic():
        user = User.objects.create_user(
            username=username or email.split("@")[0][:150],
            email=email,
            password=password,
        )
        organization = Organization.objects.create(name=organization_name)
        OrganizationMembership.objects.create(
            user=user,
            organization=organization,
            role=Role.OWNER,
            is_active=True,
        )
    return user, organization
