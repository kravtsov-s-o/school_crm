from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from lessons.filters import LessonFilter
from lessons.models import Lesson
from lessons.serializers.cabinet.student_lesson import StudentLessonCabinetSerializer


@extend_schema(tags=["Cabinet: Student Lesson"])
class StudentLessonCabinetViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StudentLessonCabinetSerializer
    filterset_class = LessonFilter
    ordering_fields = ("start_at", "status", "duration__minutes",
                       "lesson_type__name", "teacher__user__last_name")


    def get_queryset(self):
        return (Lesson.objects.filter(students__user=self.request.user)
                .select_related("teacher__user", "language", "lesson_type", "duration")
                .prefetch_related("students__user")
                .distinct())