from rest_framework import serializers

from core.serializers import BriefRelatedField
from finance.models import Account, Transaction, TransactionCode
from finance.serializers.common import AccountBriefSerializer
from school_settings.models import Currency
from school_settings.serializers.common import CurrencyBriefSerializer

MANUAL_TYPES = (TransactionCode.MANUAL_TOPUP, TransactionCode.MANUAL_PAYOUT,
                TransactionCode.CORRECTION_IN, TransactionCode.CORRECTION_OUT)


class TransactionAdminSerializer(serializers.ModelSerializer):
    account = BriefRelatedField(AccountBriefSerializer, queryset=Account.objects.all())
    currency = BriefRelatedField(CurrencyBriefSerializer, queryset=Currency.objects.all())
    type = serializers.ChoiceField(choices=[(c.value, c.label) for c in MANUAL_TYPES])
    lesson = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Transaction
        fields = ("id", "date", "account", "type", "amount", "currency", "lesson", "comment")
        read_only_fields = ("id",)
