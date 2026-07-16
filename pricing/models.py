from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _

from core._mixins import TimeStampMixin


# Create your models here.
class AbstractPrice(TimeStampMixin):
    name = models.CharField(unique=True, max_length=100, verbose_name=_("Name"))
    currency = models.ForeignKey(
        "school_settings.Currency", on_delete=models.PROTECT, verbose_name=_("Currency")
    )
    language = models.ForeignKey(
        "school_settings.Language", on_delete=models.PROTECT, verbose_name=_("Language")
    )
    lesson_type = models.ForeignKey(
        "school_settings.LessonType",
        on_delete=models.PROTECT,
        verbose_name=_("Lesson Type"),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))

    def __str__(self):
        return f"{self.name} - {self.currency.code}"

    def __repr__(self):
        return self.__str__()

    class Meta:
        abstract = True
        ordering = ["name"]
        constraints = [
            UniqueConstraint(
                fields=["currency", "language", "lesson_type"],
                name="unique_%(app_label)s_%(class)s_key",
            )
        ]


class AbstractPriceRow(TimeStampMixin):
    duration = models.ForeignKey(
        "school_settings.Duration", on_delete=models.PROTECT, verbose_name=_("Duration")
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Amount")
    )

    def __str__(self):
        return f"{self.plan} - {self.duration}"

    def __repr__(self):
        return self.__str__()

    class Meta:
        abstract = True
        constraints = [
            UniqueConstraint(
                fields=["plan", "duration"],
                name="unique_duration_per_%(app_label)s_%(class)s",
            )
        ]


class SchoolPrice(AbstractPrice):
    class Meta(AbstractPrice.Meta):
        verbose_name = _("School Price")
        verbose_name_plural = _("School Prices")
        ordering = ["name"]


class SchoolPriceRow(AbstractPriceRow):
    plan = models.ForeignKey(
        SchoolPrice,
        on_delete=models.CASCADE,
        related_name="rows",
        verbose_name=_("School Price"),
    )

    class Meta(AbstractPriceRow.Meta):
        verbose_name = _("School Price Row")
        verbose_name_plural = _("School Price Rows")
        ordering = ["plan", "duration__minutes"]


class TeacherRate(AbstractPrice):
    grade = models.ForeignKey(
        "school_settings.TeacherGrade",
        null=True,
        on_delete=models.PROTECT,
        related_name="rates",
        verbose_name=_("Grade"),
    )

    class Meta(AbstractPrice.Meta):
        verbose_name = _("Teacher Rate")
        verbose_name_plural = _("Teacher Rates")
        ordering = ["name"]

        constraints = [
            UniqueConstraint(
                fields=["grade", "currency", "language", "lesson_type"],
                name="unique_teachers_rates_key",
            )
        ]


class TeacherRateRow(AbstractPriceRow):
    plan = models.ForeignKey(
        TeacherRate,
        on_delete=models.CASCADE,
        related_name="rows",
        verbose_name=_("Teacher Rate"),
    )

    class Meta(AbstractPriceRow.Meta):
        verbose_name = _("Teacher Rate Row")
        verbose_name_plural = _("Teacher Rate Rows")
        ordering = ["plan", "duration__minutes"]


class PersonalPlan(AbstractPrice):
    duration = models.ForeignKey(
        "school_settings.Duration", on_delete=models.PROTECT, verbose_name=_("Duration")
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Amount")
    )

    class Meta(AbstractPrice.Meta):
        verbose_name = _("Personal Plan")
        verbose_name_plural = _("Personal Plans")
        constraints = []
