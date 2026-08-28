from rest_framework import serializers

from finance.serializers.common import AccountBriefSerializer


class AccountAdminSerializer(AccountBriefSerializer):
    balance = serializers.DecimalField(max_digits=12, decimal_places=2,
                                       read_only=True, source="total_balance")

    class Meta(AccountBriefSerializer.Meta):
        fields = (*AccountBriefSerializer.Meta.fields, "balance")
