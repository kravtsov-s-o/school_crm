from django.db import transaction
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from timezone_field.rest_framework import TimeZoneSerializerField

from users.models import User
from users.serializers.common import validate_password_strength


class UserAdminSerializer(serializers.ModelSerializer):
    """Admin read/update view of a ``User``: account fields, role flags, and
    group/permission assignment. Excludes the password (managed separately via
    creation and the set-password action)."""

    phone = PhoneNumberField(required=False, allow_null=True,
                             validators=[UniqueValidator(queryset=User.objects.all())])
    timezone = TimeZoneSerializerField()

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email",
                  "is_teacher", "is_student", "is_active", "is_staff", "is_superuser",
                  "timezone", "phone",
                  "groups", "user_permissions")
        read_only_fields = ("id",)


class UserAdminCreateSerializer(UserAdminSerializer):
    """Admin User creation: the read/update fields plus a write-only, validated
    ``password``."""

    password = serializers.CharField(write_only=True,
                                     validators=[validate_password_strength])

    class Meta(UserAdminSerializer.Meta):
        fields = (*UserAdminSerializer.Meta.fields, "password")

    @transaction.atomic
    def create(self, validated_data):
        """Create the User with a hashed password, then assign the M2M
        ``groups``/``user_permissions`` after the row exists."""
        password = validated_data.pop("password")

        groups = validated_data.pop("groups", [])
        perms = validated_data.pop("user_permissions", [])
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        user.groups.set(groups)
        user.user_permissions.set(perms)

        return user


class UserAdminSetPasswordSerializer(serializers.Serializer):
    """Payload for the admin set-password action: a single validated
    ``password``, no old password required."""

    password = serializers.CharField(write_only=True,
                                     validators=[validate_password_strength])
