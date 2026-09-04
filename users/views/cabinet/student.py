from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveAPIView

from users.models import StudentProfile
from users.serializers.cabinet.student import StudentCabinetSerializer


@extend_schema(tags=["Cabinet"])
class StudentCabinetView(RetrieveAPIView):
    """The signed-in user's own student profile (read-only); 404 if they have none."""

    serializer_class = StudentCabinetSerializer

    def get_object(self):
        profile = (StudentProfile.objects
                   .select_related("currency", "company", "account")
                   .prefetch_related("teacher__user", "languages", "personal_plans")
                   .filter(user=self.request.user)
                   .first())

        if profile is None:
            raise NotFound("You have no student profile.")
        return profile
