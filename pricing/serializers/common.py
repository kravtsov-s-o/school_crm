from rest_framework import serializers

from pricing.models import PersonalPlan


class PersonalPlanBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalPlan
        fields = ("id", "name")
        read_only_fields = fields
