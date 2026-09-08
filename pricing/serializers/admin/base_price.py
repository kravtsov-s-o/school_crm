from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from core.serializers import BriefRelatedField
from school_settings.models import Currency, Duration, Language, LessonType
from school_settings.serializers.common import (
    CurrencyBriefSerializer,
    DurationBriefSerializer,
    LanguageBriefSerializer,
    LessonTypeBriefSerializer,
)


class PriceRowBaseSerializer(serializers.ModelSerializer):
    """One price row (duration → amount); base for the per-type row serializers."""

    duration = BriefRelatedField(DurationBriefSerializer, queryset=Duration.objects.all())

    class Meta:
        fields = ("duration", "amount")


class PriceAdminBaseSerializer(serializers.ModelSerializer):
    """Shared price-plan fields (currency/language/lesson_type) + nested-rows
    create/update (replace-all) and duplicate-duration validation."""

    currency = BriefRelatedField(CurrencyBriefSerializer, queryset=Currency.objects.all())
    language = BriefRelatedField(LanguageBriefSerializer, queryset=Language.objects.all())
    lesson_type = BriefRelatedField(LessonTypeBriefSerializer, queryset=LessonType.objects.all())

    def validate(self, attrs):
        rows = attrs.get("rows")
        if rows:
            durations = [row["duration"] for row in rows]
            if len(durations) != len(set(durations)):
                raise serializers.ValidationError(
                    {"rows": _("Duplicate duration in rows.")}
                )
        return attrs

    def _sync_rows(self, plan, rows):
        plan.rows.all().delete()
        RowModel = plan.rows.model
        RowModel.objects.bulk_create([RowModel(plan=plan, **row) for row in rows])

    @transaction.atomic
    def create(self, validated_data):
        rows = validated_data.pop("rows", [])
        plan = super().create(validated_data)
        self._sync_rows(plan, rows)
        return plan

    @transaction.atomic
    def update(self, instance, validated_data):
        rows = validated_data.pop("rows", None)
        plan = super().update(instance, validated_data)
        if rows is not None:
            self._sync_rows(plan, rows)
        return plan
