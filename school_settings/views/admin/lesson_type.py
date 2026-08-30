from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser

from school_settings.models import LessonType
from school_settings.serializers.admin.lesson_type import LessonTypeAdminSerializer


@extend_schema(tags=["Admin: Lesson Type"])
class LessonTypeAdminViewSet(viewsets.ModelViewSet):
    """Admin CRUD for lesson types."""

    permission_classes = (IsAdminUser, DjangoModelPermissions)
    serializer_class = LessonTypeAdminSerializer
    queryset = LessonType.objects.all()
    filterset_fields = ("duration_affects_price", "is_active",)
    search_fields = ("name",)
    ordering_fields = ("name", "min_participants",
                       "max_participants", "duration_affects_price",
                       "is_active")
