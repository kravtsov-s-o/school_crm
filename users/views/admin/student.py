from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser

from users.models import StudentProfile
from users.serializers.admin.student import (
    StudentAdminCreateSerializer,
    StudentAdminListSerializer,
    StudentAdminSerializer,
)


@extend_schema(tags=["Admin: Students"])
class StudentViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = (IsAdminUser, DjangoModelPermissions)
    queryset = (StudentProfile.objects
                .select_related("user", "teacher__user", "currency", "company", "account")
                .prefetch_related("languages", "personal_plans"))

    def get_serializer_class(self):
        if self.action == "create":
            return StudentAdminCreateSerializer
        elif self.action == "list":
            return StudentAdminListSerializer
        else:
            return StudentAdminSerializer
