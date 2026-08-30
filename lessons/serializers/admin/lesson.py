from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from core.serializers import BriefRelatedField
from lessons.models import Lesson
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


class LessonAdminSerializer(serializers.ModelSerializer):
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
        read_only_fields = ("id", "status", "lesson_price")

    def validate(self, attrs):
        students = attrs.get("students")
        if students is None and self.instance is not None:
            students = list(self.instance.students.all())
        students = students or []
        lesson_type = attrs.get("lesson_type", getattr(self.instance, "lesson_type", None))

        if students:
            if len({student.currency_id for student in students}) > 1:
                raise serializers.ValidationError(
                    {"students": _("All students must have one currency.")}
                )

        if lesson_type is not None and students:
            count = len(students)
            if (lesson_type.min_participants is None
                    and lesson_type.max_participants is None and count != 1):
                raise serializers.ValidationError({"students": _("Must be exactly 1 student.")})
            if lesson_type.min_participants and count < lesson_type.min_participants:
                raise serializers.ValidationError(
                    {"students": _("Min students: {n}.").format(n=lesson_type.min_participants)})
            if lesson_type.max_participants and count > lesson_type.max_participants:
                raise serializers.ValidationError(
                    {"students": _("Max students: {n}.").format(n=lesson_type.max_participants)})
        return attrs
