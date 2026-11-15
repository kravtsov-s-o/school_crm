from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from school_settings.serializers.common import LanguageBriefSerializer
from users.models import StudentProfile


class TeacherStudentsCabinetSerializer(serializers.ModelSerializer):
    """Teacher`s Students List, teacher see it in his cabinet and lesson form
     — name, contacts (email/phone), languages, meeting_url."""

    full_name = serializers.CharField(source="user.get_full_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    phone = PhoneNumberField(source="user.phone", read_only=True)
    languages = LanguageBriefSerializer(many=True, read_only=True)

    class Meta:
        model = StudentProfile
        fields = ("id", "full_name", "email", "phone",
                  "languages", "meeting_url")
        read_only_fields = ("id",)
