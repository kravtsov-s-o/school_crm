from rest_framework import serializers

from school_settings.models import Duration


class DurationCabinetSerializer(serializers.ModelSerializer):
    """Cabinet readonly for a lesson duration."""

    class Meta:
        model = Duration
        fields = ("id", "minutes")
