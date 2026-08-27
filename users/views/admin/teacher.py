from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser

from users.models import TeacherProfile
from users.serializers.admin.teacher import (
    TeacherAdminCreateSerializer,
    TeacherAdminListSerializer,
    TeacherAdminSerializer,
)


@extend_schema(tags=["Admin: Teachers"])
class TeacherViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """Admin management of teachers — create/list/retrieve/update the whole person
    (User account + TeacherProfile) in one form. No delete: deactivate via the
    ``is_teacher`` flag / ``is_active``."""

    permission_classes = (IsAdminUser, DjangoModelPermissions)
    queryset = (TeacherProfile.objects
                .select_related("user", "currency", "account", "grade")
                .prefetch_related("languages", "lesson_types"))

    def get_serializer_class(self):
        if self.action == "create":
            return TeacherAdminCreateSerializer
        elif self.action == "list":
            return TeacherAdminListSerializer
        else:
            return TeacherAdminSerializer
