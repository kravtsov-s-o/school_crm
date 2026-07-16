from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class SystemProtectedQuerySet(models.QuerySet):
    def delete(self):
        if self.filter(is_system=True).exists():
            raise ValidationError(_("System records cannot be deleted."))
        return super().delete()


class SystemProtectedAdminMixin:
    readonly_fields = ("is_system",)

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.is_system:
            return False
        return super().has_delete_permission(request, obj)
