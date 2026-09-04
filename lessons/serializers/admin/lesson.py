from rest_framework import serializers

from core.serializers import BriefRelatedField
from lessons.models import Lesson
from lessons.serializers.common import BaseLessonSerializer
from school_settings.models import Duration, Language, LessonType
from school_settings.serializers.common import (
    CurrencyBriefSerializer,
    DurationBriefSerializer,
    LanguageBriefSerializer,
    LessonTypeBriefSerializer,
)
from users.models import StudentProfile, TeacherProfile
from users.serializers.common import StudentBriefSerializer, TeacherBriefSerializer


class LessonStatusSerializer(serializers.Serializer):
    """Input for the change-status action — the target lesson status."""

    status = serializers.ChoiceField(choices=Lesson.Status.choices)


class LessonAdminSerializer(BaseLessonSerializer):
    """Admin CRUD for a lesson's details. ``status`` / ``lesson_price`` /
    ``lesson_currency`` are read-only — status transitions go through the
    change-status action (which moves money); price/currency are derived there.
    Validates single group currency + participant count vs lesson type."""

    teacher = BriefRelatedField(TeacherBriefSerializer, queryset=TeacherProfile.objects.all())
    language = BriefRelatedField(LanguageBriefSerializer, queryset=Language.objects.all())
    lesson_type = BriefRelatedField(LessonTypeBriefSerializer, queryset=LessonType.objects.all())
    duration = BriefRelatedField(DurationBriefSerializer, queryset=Duration.objects.all())
    students = BriefRelatedField(StudentBriefSerializer, many=True,
                                 queryset=StudentProfile.objects.all())
    lesson_currency = BriefRelatedField(CurrencyBriefSerializer, read_only=True)

    class Meta:
        model = Lesson
        fields = ("id", "teacher", "language", "lesson_type",
                  "status", "start_at", "duration", "students",
                  "meeting_url", "topic", "notes", "homework",
                  "lesson_price", "lesson_currency")
        read_only_fields = ("id", "status", "lesson_price", "lesson_currency")
