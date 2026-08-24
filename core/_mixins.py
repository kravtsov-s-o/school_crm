from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from core._helpers import SystemProtectedQuerySet


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        abstract = True


class SystemRecordMixin(models.Model):
    """System records: `is_system` is frozen after creation and the record
        cannot be deleted (single via delete(), bulk via SystemProtectedQuerySet)."""

    is_system = models.BooleanField(default=False, verbose_name=_("System"))

    objects = SystemProtectedQuerySet.as_manager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.pk:
            old = type(self).objects.only("is_system").get(pk=self.pk)
            if old.is_system != self.is_system:
                raise ValidationError(
                    {"is_system": _("System flag cannot be changed.")}
                )
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.is_system:
            raise ValidationError(_("System record cannot be deleted."))
        return super().delete(*args, **kwargs)
