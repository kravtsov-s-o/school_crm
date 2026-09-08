from rest_framework import serializers

from school_settings.models import Currency, Duration, Language, LessonType, TeacherGrade


class CurrencyBriefSerializer(serializers.ModelSerializer):
    """Compact currency reference (id + code + name)."""

    class Meta:
        model = Currency
        fields = ("id", "code", "name")
        read_only_fields = fields


class LanguageBriefSerializer(serializers.ModelSerializer):
    """Compact language reference (id + name)."""

    class Meta:
        model = Language
        fields = ("id", "name")
        read_only_fields = fields


class LessonTypeBriefSerializer(serializers.ModelSerializer):
    """Compact lesson-type reference (id + name)."""

    class Meta:
        model = LessonType
        fields = ("id", "name")
        read_only_fields = fields


class TeacherGradeBriefSerializer(serializers.ModelSerializer):
    """Compact teacher-grade reference (id + name)."""

    class Meta:
        model = TeacherGrade
        fields = ("id", "name")
        read_only_fields = fields


class DurationBriefSerializer(serializers.ModelSerializer):
    """Compact duration reference (id + minutes)."""

    class Meta:
        model = Duration
        fields = ("id", "minutes")
        read_only_fields = fields
