from rest_framework import serializers

from school_settings.models import Language


class LanguageAdminSerializer(serializers.ModelSerializer):
    """Admin CRUD for a language; ``is_system`` is exposed but frozen (read-only)."""

    class Meta:
        model = Language
        fields = ("id", "name", "is_active", "is_system")
        read_only_fields = ("id", "is_system")
