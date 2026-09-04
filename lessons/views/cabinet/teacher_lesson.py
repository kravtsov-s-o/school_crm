from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.permissions import IsTeacherUser
from lessons.filters import LessonFilter
from lessons.models import Lesson
from lessons.serializers.admin.lesson import LessonStatusSerializer
from lessons.serializers.cabinet.teacher_lesson import TeacherLessonCabinetSerializer
from lessons.services import LessonChangeStatus


@extend_schema(tags=["Cabinet: Teacher Lesson"])
class TeacherLessonCabinetViewSet(viewsets.ModelViewSet):
    """A teacher's own lessons — CRUD + change-status. Teacher auto-set on create;
    only planned lessons are deletable (else 403); status transitions (which move
    money) go through the change-status action."""

    permission_classes = [IsAuthenticated, IsTeacherUser]
    serializer_class = TeacherLessonCabinetSerializer
    filterset_class = LessonFilter
    ordering_fields = ("start_at", "status", "duration__minutes",
                       "lesson_type__name", "teacher__user__last_name")

    def get_queryset(self):
        return (Lesson.objects.filter(teacher__user=self.request.user)
                .select_related("teacher__user", "language", "lesson_type", "duration")
                .prefetch_related("students__user")
                .distinct())

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user.teacherprofile)

    def perform_destroy(self, instance):
        if instance.status != Lesson.Status.PLANNED:
            raise PermissionDenied(_("Only planned lessons can be deleted."))
        instance.delete()

    @extend_schema(request=LessonStatusSerializer, responses=TeacherLessonCabinetSerializer)
    @action(detail=True, methods=["post"], url_path="change-status",
            permission_classes=[IsAuthenticated, IsTeacherUser])
    def change_status(self, request, pk=None):
        lesson = self.get_object()
        serializer = LessonStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        LessonChangeStatus(lesson, serializer.validated_data["status"]).apply()
        lesson.refresh_from_db()
        return Response(self.get_serializer(lesson).data)
