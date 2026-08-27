from rest_framework import serializers

from companies.models import Company


class CompanyBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "name")
        read_only_fields = fields
