from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveUpdateAPIView

from users.models import TeacherProfile
from users.serializers.cabinet.teacher import TeacherCabinetSerializer


@extend_schema(tags=["Cabinet"])
class TeacherCabinetView(RetrieveUpdateAPIView):
    """The signed-in user's own teacher profile — read, and edit
    ``experience_since`` / ``about_me``; 404 if they have none."""

    serializer_class = TeacherCabinetSerializer

    def get_object(self):
        profile = (TeacherProfile.objects
                   .select_related("currency", "grade", "account")
                   .prefetch_related("languages", "lesson_types")
                   .filter(user=self.request.user)
                   .first())
        if profile is None:
            raise NotFound("You have no teacher profile.")
        return profile
