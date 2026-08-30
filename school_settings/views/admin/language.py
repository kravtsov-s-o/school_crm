from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser

from school_settings.models import Language
from school_settings.serializers.admin.language import LanguageAdminSerializer


@extend_schema(tags=["Admin: Language"])
class LanguageAdminViewSet(viewsets.ModelViewSet):
    """Admin CRUD for languages. System records can't be deleted (403)."""

    permission_classes = (IsAdminUser, DjangoModelPermissions)
    serializer_class = LanguageAdminSerializer
    queryset = Language.objects.all()
    filterset_fields = ("is_active",)
    search_fields = ("name",)
    ordering_fields = ("name", "is_active")
