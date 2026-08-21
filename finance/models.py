from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core._mixins import TimeStampMixin
from finance.services import signed_amount


# Create your models here.
class Account(TimeStampMixin):
    def __str__(self):
        owner = self.owner
        return f"Account: {owner}" if owner else f"Account #{self.pk}"

    def __repr__(self):
        return self.__str__()

    @property
    def balance(self):
        return self.transactions.aggregate(s=Sum("amount"))["s"] or 0

    @property
    def owner(self):
        for name in ("student_profile", "teacher_profile", "company"):
            try:
                return getattr(self, name)
            except ObjectDoesNotExist:  # noqa: S112
                continue
        return None

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")
        ordering = ["-created_at"]


class TransactionCode(models.TextChoices):
    LESSON_CHARGE = "lesson_charge", _("Lesson charge")
    LESSON_REFUND = "lesson_refund", _("Lesson refund")
    TEACHER_REFUND = "teacher_refund", _("Teacher refund")
    TEACHER_ACCRUAL = "teacher_accrual", _("Teacher accrual")
    MANUAL_PAYOUT = "manual_payout", _("Manual payout")
    MANUAL_TOPUP = "manual_topup", _("Manual top-up")
    CORRECTION_OUT = "correction_out", _("Correction −")
    CORRECTION_IN = "correction_in", _("Correction +")

    @property
    def direction(self):
        return {
            self.LESSON_CHARGE: "expense",
            self.LESSON_REFUND: "income",
            self.TEACHER_REFUND: "expense",
            self.TEACHER_ACCRUAL: "income",
            self.MANUAL_PAYOUT: "expense",
            self.MANUAL_TOPUP: "income",
            self.CORRECTION_OUT: "expense",
            self.CORRECTION_IN: "income",
        }[self]


class AppendOnlyQuerySet(models.QuerySet):
    def update(self, **kwargs):
        raise ValidationError(
            _("Transactions are append-only; update is not allowed.")
        )

    def delete(self, **kwargs):
        raise ValidationError(
            _("Transactions are append-only; delete is not allowed.")
        )


class Transaction(TimeStampMixin):
    date = models.DateField(default=timezone.localdate, verbose_name=_("Date"))
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="transactions",
        verbose_name=_("Account"),
    )
    type = models.CharField(
        choices=TransactionCode.choices,
        max_length=15,
        verbose_name=_("Transaction Type"),
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Amount")
    )
    currency = models.ForeignKey(
        "school_settings.Currency", on_delete=models.PROTECT, verbose_name=_("Currency")
    )
    lesson = models.ForeignKey(
        "lessons.Lesson",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="transactions",
        verbose_name=_("Lesson"),
    )
    comment = models.TextField(blank=True, verbose_name=_("Comment"))

    objects = AppendOnlyQuerySet.as_manager()

    def __str__(self):
        return f"{self.date} · {self.type} · {self.amount} {self.currency.code}"

    def __repr__(self):
        return self.__str__()

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError(_("Object can't be changed."))

        self.amount = signed_amount(self.amount, self.type)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.pk:
            raise ValidationError(_("Record cannot be deleted."))

        return super().delete(*args, **kwargs)

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")
        ordering = ["-date", "-created_at"]
