"""Views for organizations and memberships."""
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.organizations.models import Organization, OrganizationMembership, Role
from apps.organizations.permissions import get_membership
from apps.organizations.serializers import (
    MembershipCreateSerializer,
    MembershipSerializer,
    MembershipUpdateSerializer,
    OrganizationCreateSerializer,
    OrganizationSerializer,
)

User = get_user_model()


class OrganizationListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        return Organization.objects.filter(
            memberships__user=self.request.user,
            memberships__is_active=True,
        ).distinct()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrganizationCreateSerializer
        return OrganizationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            org = Organization.objects.create(**serializer.validated_data)
            OrganizationMembership.objects.create(
                user=request.user, organization=org, role=Role.OWNER, is_active=True
            )
        return Response(OrganizationSerializer(org).data, status=status.HTTP_201_CREATED)


class OrganizationDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganizationSerializer
    lookup_field = "id"
    queryset = Organization.objects.all()

    def get_object(self):
        obj = super().get_object()
        membership = get_membership(self.request.user, obj.id)
        if membership is None:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied("Not a member of this organization.")
        return obj

    def update(self, request, *args, **kwargs):
        membership = get_membership(request.user, self.kwargs["id"])
        if membership is None or membership.role not in (Role.OWNER, Role.ADMIN):
            return Response(
                {"detail": "Permission denied.", "code": "permission_denied"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)




class MembershipListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MembershipSerializer

    def get_organization(self):
        org_id = self.kwargs["id"]
        membership = get_membership(self.request.user, org_id)
        if membership is None or membership.role not in (Role.OWNER, Role.ADMIN):
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied("Not authorized to manage members.")
        return Organization.objects.get(id=org_id)

    def get_queryset(self):
        org = self.get_organization()
        return OrganizationMembership.objects.filter(organization=org).select_related("user")

    def create(self, request, *args, **kwargs):
        org = self.get_organization()
        from apps.organizations.serializers import MembershipCreateSerializer

        serializer = MembershipCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(email__iexact=data["email"])
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found.", "code": "user_not_found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if OrganizationMembership.objects.filter(user=user, organization=org).exists():
            return Response(
                {"detail": "User is already a member.", "code": "duplicate_membership"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        requester = get_membership(request.user, org.id)
        requested_role = data["role"]
        if requested_role in (Role.OWNER, Role.ADMIN) and requester.role != Role.OWNER:
            return Response(
                {"detail": "Only owners can assign elevated roles.", "code": "role_escalation"},
                status=status.HTTP_403_FORBIDDEN,
            )
        membership = OrganizationMembership.objects.create(
            user=user, organization=org, role=requested_role, is_active=True
        )
        return Response(MembershipSerializer(membership).data, status=status.HTTP_201_CREATED)


class MembershipDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MembershipSerializer
    lookup_field = "membership_id"
    queryset = OrganizationMembership.objects.all()

    def get_object(self):
        org_id = self.kwargs["id"]
        requester = get_membership(self.request.user, org_id)
        if requester is None or requester.role not in (Role.OWNER, Role.ADMIN):
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied("Not authorized.")
        return OrganizationMembership.objects.get(
            id=self.kwargs["membership_id"], organization_id=org_id
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        requester = get_membership(request.user, self.kwargs["id"])
        from apps.organizations.serializers import MembershipUpdateSerializer

        serializer = MembershipUpdateSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        new_role = serializer.validated_data.get("role")
        if new_role is not None:
            if new_role in (Role.OWNER, Role.ADMIN) and requester.role != Role.OWNER:
                return Response(
                    {"detail": "Only owners can assign elevated roles.", "code": "role_escalation"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            if instance.role == Role.OWNER and new_role != Role.OWNER:
                owner_count = OrganizationMembership.objects.filter(
                    organization=instance.organization, role=Role.OWNER, is_active=True
                ).count()
                if owner_count <= 1:
                    return Response(
                        {"detail": "Cannot remove the last owner.", "code": "last_owner"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        serializer.save()
        return Response(MembershipSerializer(instance).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.role == Role.OWNER:
            owner_count = OrganizationMembership.objects.filter(
                organization=instance.organization, role=Role.OWNER, is_active=True
            ).count()
            if owner_count <= 1:
                return Response(
                    {"detail": "Cannot remove the last owner.", "code": "last_owner"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
