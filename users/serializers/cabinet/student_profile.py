from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from users.models import StudentProfile


class StudentProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    email = serializers.EmailField(source="user.email", read_only=True)
    teacher = serializers.StringRelatedField(read_only=True)
    currency = serializers.StringRelatedField(read_only=True)
    company = serializers.StringRelatedField(read_only=True)
    balance = serializers.SerializerMethodField()

    class Meta:
        model = StudentProfile
        fields = ("id", "full_name", "email", "teacher",
                  "currency", "company", "balance", "is_active")

    def get_full_name(self, obj):
        return str(obj.user)

    @extend_schema_field(serializers.DecimalField(max_digits=12, decimal_places=2))
    def get_balance(self, obj):
        return obj.account.balance if obj.account_id else 0
