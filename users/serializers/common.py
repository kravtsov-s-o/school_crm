from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from users.models import TeacherProfile, User


class UserBriefSerializer(serializers.ModelSerializer):
    """Compact read-only identity of a User (id + name + email) for embedding
    as a reference in other resources — student/teacher lists, lessons, companies."""

    full_name = serializers.CharField(source="get_full_name", read_only=True)

    class Meta:
        model = User
        fields = ("id", "full_name", "email")
        read_only_fields = fields


class TeacherBriefSerializer(serializers.ModelSerializer):
    """Compact read-only reference to a teacher — profile id + name."""

    full_name = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = TeacherProfile
        fields = ("id", "full_name")
        read_only_fields = fields


def validate_password_strength(value):
    """Run a password through Django's ``AUTH_PASSWORD_VALIDATORS``, re-raising
    any failure as a DRF error (clean 400 instead of a 500)."""
    try:
        django_validate_password(value)
    except DjangoValidationError as e:
        raise serializers.ValidationError(list(e.messages)) from e
