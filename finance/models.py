from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from core._mixins import TimeStampMixin


# Create your models here.
class Account(TimeStampMixin):
    def __str__(self):
        owner = self.owner
        return f"Account: {owner}" if owner else f"Account #{self.pk}"

    def __repr__(self):
        return self.__str__()

    @property
    def balance(self):
        pass
        # return self.transactions.aggregate(s=Sum('amount'))['s'] or 0

    @property
    def owner(self):
        for name in ("student_profile", "teacher_profile", "company"):
            try:
                return getattr(self, name)
            except ObjectDoesNotExist:  # noqa: S112 — штатный "владелец не привязан"
                continue
        return None

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")
        ordering = ["-created_at"]
