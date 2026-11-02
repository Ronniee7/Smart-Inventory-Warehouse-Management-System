"""URL routes for organizations and memberships."""
from django.urls import path

from apps.organizations.views import (
    MembershipDetailView,
    MembershipListCreateView,
    OrganizationDetailView,
    OrganizationListCreateView,
)

urlpatterns = [
    path("organizations/", OrganizationListCreateView.as_view(), name="organization-list"),
    path("organizations/<uuid:id>/", OrganizationDetailView.as_view(), name="organization-detail"),
    path(
        "organizations/<uuid:id>/members/",
        MembershipListCreateView.as_view(),
        name="organization-members",
    ),
    path(
        "organizations/<uuid:id>/members/<uuid:membership_id>/",
        MembershipDetailView.as_view(),
        name="organization-member-detail",
    ),
]
