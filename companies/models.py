from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core._mixins import TimeStampMixin


# Create your models here.
class Company(TimeStampMixin):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    currency = models.ForeignKey(
        "school_settings.Currency", on_delete=models.PROTECT, verbose_name=_("Currency")
    )
    account = models.OneToOneField(
        "finance.Account",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="company",
        verbose_name=_("Account"),
    )
    personal_plans = models.ManyToManyField(
        "pricing.PersonalPlan",
        blank=True,
        verbose_name=_("Personal Plan"),
        help_text=_(
            "The personal plan for this company."
            "If company price must be different from the school plan."
        ),
    )
    coverage_percent = models.PositiveSmallIntegerField(
        default=100,
        verbose_name=_("Coverage percent"),
        validators=[MaxValueValidator(100), MinValueValidator(0)],
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
        ordering = ["name"]
