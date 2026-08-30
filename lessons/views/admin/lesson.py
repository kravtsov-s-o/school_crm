from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser
from rest_framework.response import Response

from lessons.models import Lesson
from lessons.serializers.admin.lesson import LessonAdminSerializer, LessonStatusSerializer
from lessons.services import LessonChangeStatus


@extend_schema(tags=["Admin: Lesson"])
class LessonAdminViewSet(viewsets.ModelViewSet):
    """Admin CRUD for lessons. Status is read-only here — transitions
    (which move money)
    go through the change-status action. Only planned lessons can be deleted."""

    permission_classes = (IsAdminUser, DjangoModelPermissions)
    serializer_class = LessonAdminSerializer
    queryset = (Lesson.objects
                .select_related("teacher__user", "language", "lesson_type",
                                "duration", "lesson_currency")
                .prefetch_related("students__user"))

    def perform_destroy(self, instance):
        if instance.status != Lesson.Status.PLANNED:
            raise PermissionDenied(_("Only planned lessons can be deleted."))
        instance.delete()

    @extend_schema(request=LessonStatusSerializer, responses=LessonAdminSerializer)
    @action(detail=True, methods=["post"], url_path="change-status",
            permission_classes=[IsAdminUser])
    def change_status(self, request, pk=None):
        lesson = self.get_object()
        serializer = LessonStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        LessonChangeStatus(lesson, serializer.validated_data["status"]).apply()
        lesson.refresh_from_db()
        return Response(self.get_serializer(lesson).data)
