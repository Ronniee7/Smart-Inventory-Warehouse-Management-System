"""Organization models for StockPilot."""
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "organizations_organization"
        ordering = ["name"]
        constraints = [
            models.CheckConstraint(
                check=~models.Q(name=""),
                name="organization_name_not_empty",
            ),
        ]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or "organization"
            candidate = base
            counter = 1
            while Organization.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base}-{counter}"
                counter += 1
            self.slug = candidate
        super().save(*args, **kwargs)


class Role(models.TextChoices):
    OWNER = "owner", "Owner"
    ADMIN = "admin", "Administrator"
    MANAGER = "manager", "Manager"
    STAFF = "staff", "Staff"
    VIEWER = "viewer", "Viewer"


class OrganizationMembership(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.VIEWER)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "organizations_membership"
        ordering = ["-joined_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "organization"],
                name="unique_user_organization_membership",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user} - {self.organization} ({self.role})"
