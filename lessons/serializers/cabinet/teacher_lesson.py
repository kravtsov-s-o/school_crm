from core.serializers import BriefRelatedField
from lessons.models import Lesson
from lessons.serializers.common import BaseLessonSerializer
from school_settings.models import Duration, Language, LessonType
from school_settings.serializers.common import (
    DurationBriefSerializer,
    LanguageBriefSerializer,
    LessonTypeBriefSerializer,
)
from users.models import StudentProfile
from users.serializers.common import StudentBriefSerializer, TeacherBriefSerializer


class TeacherLessonCabinetSerializer(BaseLessonSerializer):
    """A teacher's own lesson (create/edit). ``teacher`` is read-only (injected by
    the view); ``students`` are limited to the teacher's own; once the lesson is no
    longer PLANNED only ``topic``/``notes``/``homework`` stay editable."""

    teacher = TeacherBriefSerializer(read_only=True)
    language = BriefRelatedField(LanguageBriefSerializer, queryset=Language.objects.all())
    lesson_type = BriefRelatedField(LessonTypeBriefSerializer, queryset=LessonType.objects.all())
    duration = BriefRelatedField(DurationBriefSerializer, queryset=Duration.objects.all())
    students = BriefRelatedField(StudentBriefSerializer, many=True,
                                 queryset=StudentProfile.objects.all())

    class Meta:
        model = Lesson
        fields = ("id", "teacher", "language", "lesson_type", "status", "start_at",
                  "duration", "students", "meeting_url", "topic", "notes", "homework")
        read_only_fields = ("id", "status")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request is not None:
            self.fields["students"].child_relation.queryset = (
                request.user.teacherprofile.students.all()
            )
        if self.instance and getattr(self.instance, "status", None) != Lesson.Status.PLANNED:
            editable = {"topic", "notes", "homework"}
            for name, field in self.fields.items():
                if name not in editable:
                    field.read_only = True
