from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions

from school_settings.models import LessonType
from school_settings.serializers.admin.lesson_type import LessonTypeAdminSerializer


@extend_schema(tags=["Admin: Lesson Type"])
class LessonTypeAdminViewSet(viewsets.ModelViewSet):
    """Admin CRUD for lesson types."""

    permission_classes = (IsAdminUser, DjangoModelPermissions)
    serializer_class = LessonTypeAdminSerializer
    queryset = LessonType.objects.all()
