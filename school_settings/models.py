from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint, Q, F
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from core._mixins import TimeStampMixin, SystemRecordMixin


# Create your models here.
class Language(TimeStampMixin, SystemRecordMixin):
    name = models.CharField(unique=True, max_length=100, verbose_name=_('Name'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')
        ordering = ('-is_active', 'name')

        constraints = [
            UniqueConstraint(
                fields=['is_system'],
                condition=Q(is_system=True),
                name='unique_system_language',
            ),
        ]


class Currency(TimeStampMixin, SystemRecordMixin):
    code = models.CharField(unique=True, max_length=4, verbose_name=_('Code'))
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    symbol = models.CharField(max_length=2, null=True, blank=True, verbose_name=_('Symbol'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))

    def __str__(self):
        return self.code

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')
        ordering = ('-is_active', 'name')

        constraints = [
            UniqueConstraint(
                fields=['is_system'],
                condition=Q(is_system=True),
                name='unique_system_currency',
            ),
        ]


class ExchangeRate(TimeStampMixin):
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='rates', verbose_name=_('Currency'))
    rate = models.DecimalField(max_digits=18, decimal_places=8, verbose_name=_('Rate'))
    date = models.DateField(verbose_name=_('Date'))

    def __str__(self):
        return f"{self.currency.code} {self.rate} ({self.date})"

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = _('Exchange Rate')
        verbose_name_plural = _('Exchange Rates')
        ordering = ('-date', 'currency__code')
        constraints = [
            UniqueConstraint(
                fields=['currency', 'date'],
                name='unique_rate_per_currency_per_date',
            )
        ]


class Duration(TimeStampMixin, SystemRecordMixin):
    minutes = models.PositiveSmallIntegerField(unique=True, verbose_name=_('Minutes'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))

    def __str__(self):
        return f"{self.minutes} min"

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = _('Duration')
        verbose_name_plural = _('Durations')
        ordering = ('-is_active', 'minutes')

        constraints = [
            UniqueConstraint(
                fields=['is_system'],
                condition=Q(is_system=True),
                name='unique_system_duration',
            ),
        ]


class LessonType(TimeStampMixin):
    name = models.CharField(unique=True, max_length=100, verbose_name=_('Name'))
    min_participants = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_('Min. Participants'))
    max_participants = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_('Max. Participants'))
    duration_affects_price = models.BooleanField(
        default=True,
        verbose_name=_('Duration Affects Price'),
        help_text=mark_safe(_('If enabled, duration is part of the price key: <br>'
                    '45 and 60 min are priced differently. If disabled, price does not depend on duration.')),
    )
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = _('Lesson Type')
        verbose_name_plural = _('Lesson Types')
        ordering = ('-is_active', 'name')

        constraints = [
            CheckConstraint(
                condition=Q(max_participants__gte=F('min_participants')),
                name='lessontype_max_gte_min',
            ),
        ]