from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from school_settings.serializers.common import LanguageBriefSerializer
from users.models import TeacherProfile


class TeacherCardCabinetSerializer(serializers.ModelSerializer):
    """Public teacher card a student sees — name, contacts (email/phone),
    about_me, languages, experience. No grade/currency/balance."""

    full_name = serializers.CharField(source="user.get_full_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    phone = PhoneNumberField(source="user.phone", read_only=True)
    languages = LanguageBriefSerializer(many=True, read_only=True)

    class Meta:
        model = TeacherProfile
        fields = ("id", "full_name", "email", "phone",
                  "languages", "about_me", "experience_since")
