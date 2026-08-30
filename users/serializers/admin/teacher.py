from django.db import transaction
from rest_framework import serializers

from core.serializers import BriefRelatedField
from school_settings.models import Currency, Language, LessonType, TeacherGrade
from school_settings.serializers.common import (
    CurrencyBriefSerializer,
    LanguageBriefSerializer,
    LessonTypeBriefSerializer,
    TeacherGradeBriefSerializer,
)
from users.models import TeacherProfile
from users.serializers.admin.user import UserAdminCreateSerializer, UserAdminSerializer
from users.serializers.common import UserBriefSerializer


class TeacherAdminListSerializer(serializers.ModelSerializer):
    """Compact teacher row for the admin list — identity plus key columns."""

    user = UserBriefSerializer(read_only=True)
    currency = CurrencyBriefSerializer(read_only=True)
    grade = TeacherGradeBriefSerializer(read_only=True)
    balance = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = TeacherProfile
        fields = ("id", "user", "grade", "balance", "currency", "is_active")


class TeacherAdminBaseSerializer(serializers.ModelSerializer):
    """Shared teacher-profile fields for the admin create/update serializers;
    FK/M2M exposed as writable brief refs (PK in, ``{id, label}`` out)."""

    currency = BriefRelatedField(CurrencyBriefSerializer, queryset=Currency.objects.all())
    languages = BriefRelatedField(LanguageBriefSerializer, many=True,
                                  queryset=Language.objects.all())
    lesson_types = BriefRelatedField(LessonTypeBriefSerializer, many=True,
                                     queryset=LessonType.objects.all())
    grade = BriefRelatedField(TeacherGradeBriefSerializer, queryset=TeacherGrade.objects.all())
    balance = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = TeacherProfile
        fields = ("id", "user", "languages", "lesson_types", "grade", "currency",
                  "experience_since", "about_me", "balance", "is_active")
        read_only_fields = ("id",)


class TeacherAdminCreateSerializer(TeacherAdminBaseSerializer):
    """Admin teacher creation in one form: nested user (with password) + profile.
    Sets ``is_teacher`` so the signal makes the profile, which ``create()`` fills."""

    user = UserAdminCreateSerializer()

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data["is_teacher"] = True
        user = self.fields["user"].create(user_data)

        languages = validated_data.pop("languages", [])
        lesson_types = validated_data.pop("lesson_types", [])

        profile = user.teacherprofile
        for attr, value in validated_data.items():
            setattr(profile, attr, value)
        profile.save()
        profile.languages.set(languages)
        profile.lesson_types.set(lesson_types)
        return profile


class TeacherAdminSerializer(TeacherAdminBaseSerializer):
    """Admin teacher retrieve/update: nested editable user + profile fields,
    updated together in one atomic call."""

    user = UserAdminSerializer()

    @transaction.atomic
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        if user_data:
            self.fields["user"].update(instance.user, user_data)
        return super().update(instance, validated_data)

    def to_internal_value(self, data):
        if self.instance:
            self.fields["user"].instance = self.instance.user
        return super().to_internal_value(data)
