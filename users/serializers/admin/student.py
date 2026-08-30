from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from companies.models import Company
from companies.serializers.common import CompanyBriefSerializer
from core.serializers import BriefRelatedField
from pricing.models import PersonalPlan
from pricing.serializers.common import PersonalPlanBriefSerializer
from school_settings.models import Currency, Language
from school_settings.serializers.common import CurrencyBriefSerializer, LanguageBriefSerializer
from users.models import StudentProfile, TeacherProfile
from users.serializers.admin.user import UserAdminCreateSerializer, UserAdminSerializer
from users.serializers.common import TeacherBriefSerializer, UserBriefSerializer


class StudentAdminListSerializer(serializers.ModelSerializer):
    """Compact student row for the admin list — identity plus key columns."""

    user = UserBriefSerializer(read_only=True)
    teacher = TeacherBriefSerializer(read_only=True)
    currency = CurrencyBriefSerializer(read_only=True)
    balance = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = StudentProfile
        fields = ("id", "user", "teacher", "balance", "currency", "is_active")


class StudentAdminBaseSerializer(serializers.ModelSerializer):
    """Shared student-profile fields for the admin create/update serializers;
    FK/M2M exposed as writable brief refs (PK in, ``{id, label}`` out)."""

    currency = BriefRelatedField(CurrencyBriefSerializer, queryset=Currency.objects.all())
    languages = BriefRelatedField(LanguageBriefSerializer, many=True,
                                  queryset=Language.objects.all())
    company = BriefRelatedField(CompanyBriefSerializer, required=False, allow_null=True,
                                queryset=Company.objects.all())
    teacher = BriefRelatedField(TeacherBriefSerializer, queryset=TeacherProfile.objects.all())
    personal_plans = BriefRelatedField(PersonalPlanBriefSerializer, required=False, many=True,
                                       queryset=PersonalPlan.objects.all())
    balance = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = StudentProfile
        fields = ("id", "user", "teacher", "languages", "company", "personal_plans",
                  "balance", "currency", "meeting_url", "is_active")
        read_only_fields = ("id",)

    def validate(self, attrs):
        currency = attrs.get("currency", getattr(self.instance, "currency", None))
        company = attrs.get("company", getattr(self.instance, "company", None))

        if company is not None and currency is not None and company.currency_id != currency.id:
            raise serializers.ValidationError(
                {"currency": _("Student currency must match company currency.")}
            )

        if "personal_plans" in attrs:
            plans = attrs["personal_plans"]
        elif self.instance is not None:
            plans = self.instance.personal_plans.all()
        else:
            plans = []

        if currency is not None and any(p.currency_id != currency.id for p in plans):
            raise serializers.ValidationError(
                {"personal_plans": _("All plans must match the student currency.")}
            )
        return attrs


class StudentAdminCreateSerializer(StudentAdminBaseSerializer):
    """Admin student creation in one form: nested user (with password) + profile.
    Sets ``is_student`` so the signal makes the profile, which ``create()`` fills."""

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
    """Admin student retrieve/update: nested editable user + profile fields,
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
