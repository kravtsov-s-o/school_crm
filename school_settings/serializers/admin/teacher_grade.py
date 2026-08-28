from rest_framework import serializers

from school_settings.models import TeacherGrade


class TeacherGradeAdminSerializer(serializers.ModelSerializer):
    """Admin CRUD for a teacher grade (name + sort order)."""

    class Meta:
        model = TeacherGrade
        fields = ("id", "name", "sort_order", "is_active")
        read_only_fields = ("id",)
