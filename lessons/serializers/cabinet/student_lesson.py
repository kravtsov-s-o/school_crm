from rest_framework import serializers

from lessons.models import Lesson
from school_settings.serializers.common import (
    DurationBriefSerializer,
    LanguageBriefSerializer,
    LessonTypeBriefSerializer,
)
from users.serializers.common import StudentBriefSerializer, TeacherBriefSerializer


class StudentLessonCabinetListSerializer(serializers.ModelSerializer):
    """Read-only view of a lesson list for a student (their own lessons)."""

    teacher = TeacherBriefSerializer(read_only=True)
    language = LanguageBriefSerializer(read_only=True)
    lesson_type = LessonTypeBriefSerializer(read_only=True)
    duration = DurationBriefSerializer(read_only=True)
    students = StudentBriefSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ("id", "teacher", "language", "lesson_type",
                  "status", "start_at", "duration", "students",
                  "topic")


class StudentLessonCabinetSerializer(StudentLessonCabinetListSerializer):
    """Read-only view of a lesson for a student (their own lessons)."""

    class Meta(StudentLessonCabinetListSerializer.Meta):
        model = Lesson
        fields = (*StudentLessonCabinetListSerializer.Meta.fields,
                  "meeting_url", "notes", "homework")
        read_only_fields = fields
