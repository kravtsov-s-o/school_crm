from rest_framework import serializers

from school_settings.models import Currency, Language, LessonType, TeacherGrade, Duration


class CurrencyBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ("id", "code", "name")
        read_only_fields = fields


class LanguageBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ("id", "name")
        read_only_fields = fields


class LessonTypeBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonType
        fields = ("id", "name")
        read_only_fields = fields


class TeacherGradeBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherGrade
        fields = ("id", "name")
        read_only_fields = fields


class DurationBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Duration
        fields = ("id", "minutes")
        read_only_fields = fields
