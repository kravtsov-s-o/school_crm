from rest_framework import serializers

from school_settings.models import Duration


class DurationAdminSerializer(serializers.ModelSerializer):
    """Admin CRUD for a lesson duration; ``is_system`` is exposed but frozen."""

    class Meta:
        model = Duration
        fields = ("id", "minutes", "is_active", "is_system")
        read_only_fields = ("id", "is_system")
