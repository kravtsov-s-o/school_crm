from rest_framework import serializers

from lessons.models import Lesson
from school_settings.serializers.common import LanguageBriefSerializer, LessonTypeBriefSerializer, \
    DurationBriefSerializer
from users.serializers.common import TeacherBriefSerializer, StudentBriefSerializer


class StudentLessonCabinetSerializer(serializers.ModelSerializer):
    teacher = TeacherBriefSerializer(read_only=True)
    language = LanguageBriefSerializer(read_only=True)
    lesson_type = LessonTypeBriefSerializer(read_only=True)
    duration = DurationBriefSerializer(read_only=True)
    students = StudentBriefSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ("id", "teacher", "language", "lesson_type",
                  "status", "start_at", "duration", "students",
                  "meeting_url", "topic", "notes", "homework")
        read_only_fields = fields
