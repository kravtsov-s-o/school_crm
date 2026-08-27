from rest_framework import serializers

from users.models import User


class AccountSerializer(serializers.ModelSerializer):
    timezone = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id", "email", "first_name", "last_name", "username",
            "timezone", "phone",
            "is_student", "is_teacher", "is_staff", "is_superuser",
        )

    def get_timezone(self, obj) -> str:
        return str(obj.timezone)

    def get_phone(self, obj) -> str | None:
        return str(obj.phone) if obj.phone else None
