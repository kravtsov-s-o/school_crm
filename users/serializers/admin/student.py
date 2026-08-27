from django.db import transaction
from rest_framework import serializers

from companies.models import Company
from companies.serializers.common import CompanyBriefSerializer
from pricing.models import PersonalPlan
from pricing.serializers.common import PersonalPlanBriefSerializer
from school_settings.models import Currency, Language
from school_settings.serializers.common import CurrencyBriefSerializer, LanguageBriefSerializer
from users.models import StudentProfile, TeacherProfile
from users.serializers.admin.user import UserAdminCreateSerializer, UserAdminSerializer
from users.serializers.common import (
    BalanceSerializerMixin,
    BriefRelatedField,
    TeacherBriefSerializer,
    UserBriefSerializer,
)


class StudentAdminListSerializer(BalanceSerializerMixin, serializers.ModelSerializer):
    user = UserBriefSerializer(read_only=True)
    teacher = TeacherBriefSerializer(read_only=True)
    currency = CurrencyBriefSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = ("id", "user", "teacher", "balance", "currency", "is_active")


class StudentAdminBaseSerializer(BalanceSerializerMixin, serializers.ModelSerializer):
    currency = BriefRelatedField(CurrencyBriefSerializer, queryset=Currency.objects.all())
    languages = BriefRelatedField(LanguageBriefSerializer, many=True,
                                  queryset=Language.objects.all())
    company = BriefRelatedField(CompanyBriefSerializer, required=False, allow_null=True,
                                queryset=Company.objects.all())
    teacher = BriefRelatedField(TeacherBriefSerializer, queryset=TeacherProfile.objects.all())
    personal_plans = BriefRelatedField(PersonalPlanBriefSerializer, required=False, many=True,
                                       queryset=PersonalPlan.objects.all())

    class Meta:
        model = StudentProfile
        fields = ("id", "user", "teacher", "languages", "company", "personal_plans",
                  "balance", "currency", "meeting_url", "is_active")
        read_only_fields = ("id",)


class StudentAdminCreateSerializer(StudentAdminBaseSerializer):
    user = UserAdminCreateSerializer()

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data["is_student"] = True
        user = self.fields["user"].create(user_data)

        languages = validated_data.pop("languages", [])
        plans = validated_data.pop("personal_plans", [])

        profile = user.studentprofile
        for attr, value in validated_data.items():
            setattr(profile, attr, value)
        profile.save()
        profile.languages.set(languages)
        profile.personal_plans.set(plans)
        return profile


class StudentAdminSerializer(StudentAdminBaseSerializer):
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
