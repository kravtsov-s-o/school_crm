from rest_framework import serializers

from school_settings.models import LessonType


class LessonTypeAdminSerializer(serializers.ModelSerializer):
    """Admin CRUD for a lesson type (participant bounds + duration-affects-price)."""

    class Meta:
        model = LessonType
        fields = ("id", "name", "min_participants",
                  "max_participants", "duration_affects_price", "is_active")
        read_only_fields = ("id",)

    def validate(self, attrs):
        min_p = attrs.get("min_participants",
                        getattr(self.instance, "min_participants", None))
        max_p = attrs.get("max_participants",
                        getattr(self.instance, "max_participants", None))

        if min_p is not None and max_p is not None and max_p < min_p:
            raise serializers.ValidationError(
                {"max_participants": "Max participants must be ≥ min participants."}
            )
        return attrs
