from rest_framework import serializers

from finance.models import Account


class AccountBriefSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ("id", "owner")

    def get_owner(self, obj) -> str | None:
        return str(obj.owner) if obj.owner else None
