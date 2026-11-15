from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from school_settings.models import Duration
from school_settings.serializers.cabinet.duration import DurationCabinetSerializer


@extend_schema(tags=["Cabinet: Duration"])
class DurationCabinetViewSet(viewsets.ReadOnlyModelViewSet):
    """Cabinet readonly for lesson durations.."""

    serializer_class = DurationCabinetSerializer
    queryset = Duration.objects.filter(is_active=True)
    ordering_fields = ("minutes",)
