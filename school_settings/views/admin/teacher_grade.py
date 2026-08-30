from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser

from school_settings.models import TeacherGrade
from school_settings.serializers.admin.teacher_grade import TeacherGradeAdminSerializer


@extend_schema(tags=["Admin: Teacher Grade"])
class TeacherGradeAdminViewSet(viewsets.ModelViewSet):
    """Admin CRUD for teacher grades."""

    permission_classes = (IsAdminUser, DjangoModelPermissions)
    serializer_class = TeacherGradeAdminSerializer
    queryset = TeacherGrade.objects.all()
    filterset_fields = ("is_active",)
    search_fields = ("name",)
    ordering_fields = ("sort_order", "name", "is_active")
