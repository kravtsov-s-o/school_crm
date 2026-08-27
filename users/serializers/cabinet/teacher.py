from rest_framework import serializers

from school_settings.serializers.common import (
    CurrencyBriefSerializer,
    LanguageBriefSerializer,
    LessonTypeBriefSerializer,
    TeacherGradeBriefSerializer,
)
from users.models import TeacherProfile
from users.serializers.common import BalanceSerializerMixin


class TeacherCabinetSerializer(BalanceSerializerMixin, serializers.ModelSerializer):
    """The signed-in user's own teacher profile — read-only except the teacher's
    own ``experience_since`` / ``about_me``."""

    currency = CurrencyBriefSerializer(read_only=True)
    grade = TeacherGradeBriefSerializer(read_only=True)
    languages = LanguageBriefSerializer(many=True, read_only=True)
    lesson_types = LessonTypeBriefSerializer(many=True, read_only=True)

    class Meta:
        model = TeacherProfile
        fields = ("id", "currency", "grade", "languages", "lesson_types",
                  "experience_since", "about_me", "balance", "is_active")
        read_only_fields = ("id", "is_active")
