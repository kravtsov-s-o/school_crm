from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from users.models import TeacherProfile
from users.serializers.cabinet.teacher_card import TeacherCardCabinetSerializer


@extend_schema(tags=["Cabinet: Teacher Card"])
class TeacherCardCabinetViewSet(viewsets.ReadOnlyModelViewSet):
    """The signed-in student's own teacher(s) — read-only card list + detail."""

    serializer_class = TeacherCardCabinetSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return TeacherProfile.objects.none()

        return (TeacherProfile.objects
                .filter(students__user=self.request.user)
                .select_related("user")
                .prefetch_related("languages")
                .distinct())
