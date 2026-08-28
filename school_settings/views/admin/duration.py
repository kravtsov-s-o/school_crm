from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser

from school_settings.models import Duration
from school_settings.serializers.admin.duration import DurationAdminSerializer


@extend_schema(tags=["Admin: Duration"])
class DurationAdminViewSet(viewsets.ModelViewSet):
    """Admin CRUD for lesson durations. System records can't be deleted (403)."""

    permission_classes = (IsAdminUser, DjangoModelPermissions)
    serializer_class = DurationAdminSerializer
    queryset = Duration.objects.all()
