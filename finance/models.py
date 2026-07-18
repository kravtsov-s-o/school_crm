from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core._mixins import SystemRecordMixin, TimeStampMixin


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


class TransactionType(TimeStampMixin, SystemRecordMixin):
    class Direction(models.TextChoices):
        INCOME = "income", _("Income")
        EXPENSE = "expense", _("Expense")

    name = models.CharField(
        unique=True, max_length=100, verbose_name=_("Transaction Type")
    )
    code = models.SlugField(
        unique=True, max_length=100, verbose_name=_("Transaction Code")
    )
    direction = models.CharField(
        choices=Direction.choices, max_length=10, verbose_name=_("Direction")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = _("Transaction Type")
        verbose_name_plural = _("Transaction Types")
        ordering = ["name"]


class Transaction(TimeStampMixin):
    date = models.DateField(default=timezone.localdate, verbose_name=_("Date"))
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="transactions",
        verbose_name=_("Account"),
    )
    type = models.ForeignKey(
        TransactionType,
        on_delete=models.PROTECT,
        related_name="transactions",
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

    def __str__(self):
        return f"{self.date} · {self.type.name} · {self.amount} {self.currency.code}"

    def __repr__(self):
        return self.__str__()

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError(_("Object can't be changed."))

        self.amount = abs(self.amount)
        if self.type.direction == TransactionType.Direction.EXPENSE:
            self.amount = -self.amount

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.pk:
            raise ValidationError(_("Record cannot be deleted."))

        return super().delete(*args, **kwargs)

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")
        ordering = ["-date", "-created_at"]
