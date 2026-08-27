from decimal import Decimal

from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from drf_spectacular.utils import extend_schema_field
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


class BalanceSerializerMixin(serializers.Serializer):
    """Adds a read-only ``balance`` field — the linked Account's balance, or 0."""
    balance = serializers.SerializerMethodField()

    @extend_schema_field(serializers.DecimalField(max_digits=12, decimal_places=2))
    def get_balance(self, obj) -> Decimal:
        return obj.account.balance if obj.account_id else Decimal("0.00")


class BriefRelatedField(serializers.PrimaryKeyRelatedField):
    """Accept a PK on write; returns the brief serializer's dict on read."""

    def __init__(self, brief_serializer, **kwargs):
        self.brief_serializer = brief_serializer
        super().__init__(**kwargs)

    def use_pk_only_optimization(self):
        return False

    def to_representation(self, value):
        return self.brief_serializer(value).data

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}
        if cutoff is not None:
            queryset = queryset[:cutoff]
        return {item.pk: self.display_value(item) for item in queryset}


def validate_password_strength(value):
    """Run a password through Django's ``AUTH_PASSWORD_VALIDATORS``, re-raising
    any failure as a DRF error (clean 400 instead of a 500)."""
    try:
        django_validate_password(value)
    except DjangoValidationError as e:
        raise serializers.ValidationError(list(e.messages)) from e
