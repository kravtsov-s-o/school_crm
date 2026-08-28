from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from companies.models import Company
from core.serializers import BalanceSerializerMixin, BriefRelatedField
from pricing.models import PersonalPlan
from pricing.serializers.common import PersonalPlanBriefSerializer
from school_settings.models import Currency
from school_settings.serializers.common import CurrencyBriefSerializer


class CompanyAdminSerializer(BalanceSerializerMixin, serializers.ModelSerializer):
    """Admin CRUD for a company — currency, coverage percent, and optional
    personal plans (validated to match the company currency)."""

    currency = BriefRelatedField(CurrencyBriefSerializer, queryset=Currency.objects.all())
    personal_plans = BriefRelatedField(PersonalPlanBriefSerializer, required=False, many=True,
                                       queryset=PersonalPlan.objects.all())

    class Meta:
        model = Company
        fields = ("id", "name", "balance", "currency",
                  "personal_plans", "coverage_percent", "is_active")

    def validate(self, attrs):
        currency = attrs.get("currency", getattr(self.instance, "currency", None))

        if "personal_plans" in attrs:
            plans = attrs["personal_plans"]
        elif self.instance is not None:
            plans = self.instance.personal_plans.all()
        else:
            plans = []

        if currency is not None and any(p.currency_id != currency.id for p in plans):
            raise serializers.ValidationError(
                {"personal_plans": _("All plans must match the company currency.")}
            )
        return attrs
