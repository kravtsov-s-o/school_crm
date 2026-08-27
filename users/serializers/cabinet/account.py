from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from timezone_field.rest_framework import TimeZoneSerializerField

from users.models import User


class AccountCabinetSerializer(serializers.ModelSerializer):
    """The signed-in user's own account: personal fields (name, phone, timezone)
    editable; email/username and role flags read-only."""

    phone = PhoneNumberField(required=False, allow_null=True,
                             validators=[UniqueValidator(queryset=User.objects.all())])
    timezone = TimeZoneSerializerField()

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "username",
                  "timezone", "phone",
                  "is_student", "is_teacher", "is_staff", "is_superuser")
        read_only_fields = ("id", "email", "is_student", "is_teacher",
                            "is_staff", "is_superuser")
