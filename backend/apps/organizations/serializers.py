"""Serializers for organizations."""
from rest_framework import serializers

from apps.organizations.models import Organization, OrganizationMembership, Role


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ("id", "name", "slug", "description", "is_active", "created_at", "updated_at")
        read_only_fields = ("id", "slug", "created_at", "updated_at")


class OrganizationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ("name", "description")

    def create(self, validated_data):
        org = Organization.objects.create(**validated_data)
        return org


class MembershipSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = OrganizationMembership
        fields = ("id", "user", "email", "username", "role", "is_active", "joined_at")
        read_only_fields = ("id", "user", "email", "username", "joined_at")


class MembershipCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=Role.choices, default=Role.VIEWER)


class MembershipUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationMembership
        fields = ("role", "is_active")
