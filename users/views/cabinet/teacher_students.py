from rest_framework import mixins, viewsets
from drf_spectacular.utils import extend_schema
from users.models import StudentProfile
from users.serializers.cabinet.teacher_students import TeacherStudentsCabinetSerializer


@extend_schema(tags=["Cabinet: Teacher Students"])
class TeacherStudentsViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = TeacherStudentsCabinetSerializer

    def get_queryset(self):
        if getattr(self.request, "swagger_fake_view", False):
            return StudentProfile.objects.none()

        return (StudentProfile.objects
                .filter(teacher__user=self.request.user)
                .select_related("user")
                .distinct()
                .order_by(
                    "user__first_name",
                    "user__last_name"))

    http_method_names = ["get", "patch", "head", "options"]