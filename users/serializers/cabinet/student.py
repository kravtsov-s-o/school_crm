from rest_framework import serializers

from companies.serializers.common import CompanyBriefSerializer
from core.serializers import BalanceSerializerMixin
from pricing.serializers.common import PersonalPlanBriefSerializer
from school_settings.serializers.common import CurrencyBriefSerializer, LanguageBriefSerializer
from users.models import StudentProfile
from users.serializers.common import TeacherBriefSerializer


class StudentCabinetSerializer(BalanceSerializerMixin, serializers.ModelSerializer):
    """The signed-in user's own student profile — read-only."""

    teacher = TeacherBriefSerializer(read_only=True)
    currency = CurrencyBriefSerializer(read_only=True)
    company = CompanyBriefSerializer(read_only=True)
    languages = LanguageBriefSerializer(many=True, read_only=True)
    personal_plans = PersonalPlanBriefSerializer(many=True, read_only=True)

    class Meta:
        model = StudentProfile
        fields = ("id", "teacher", "currency", "languages", "personal_plans",
                  "company", "meeting_url", "balance", "is_active")
