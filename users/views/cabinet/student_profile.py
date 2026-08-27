from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveAPIView

from users.models import StudentProfile
from users.serializers.cabinet.student_profile import StudentProfileSerializer


class StudentProfileView(RetrieveAPIView):
    serializer_class = StudentProfileSerializer

    def get_object(self):
        profile = StudentProfile.objects.filter(user=self.request.user).first()
        if profile is None:
            raise NotFound("You have no student profile.")
        return profile
