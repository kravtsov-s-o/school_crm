from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from pricing.models import SchoolPriceRow, SchoolPrice, TeacherRate, TeacherRateRow, PersonalPlan
from school_settings.models import Duration


# Register your models here.
class BasePriceRowInline(admin.TabularInline):
    extra = 0
    verbose_name = _('Price Row')
    fields = ('duration', 'amount')

class SchoolPriceRowInline(BasePriceRowInline):
    model = SchoolPriceRow

class TeacherRateRowInline(BasePriceRowInline):
    model = TeacherRateRow


class BasePriceAdmin(admin.ModelAdmin):
    list_display = ("name", "price_per_hour", "currency", "language", "lesson_type", "is_active")
    list_filter = ("currency", "language", "lesson_type")
    search_fields = ("name",)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('rows__duration')

    @admin.display(description=_('Price / hour'))
    def price_per_hour(self, obj):
        for row in obj.rows.all():
            if row.duration.minutes == 60:
                return row.amount
        return '—'


@admin.register(SchoolPrice)
class SchoolPriceAdmin(BasePriceAdmin):
    inlines = [SchoolPriceRowInline]


@admin.register(TeacherRate)
class TeacherRateAdmin(BasePriceAdmin):
    inlines = [TeacherRateRowInline]


@admin.register(PersonalPlan)
class PersonalPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "language", "lesson_type", "is_active")
    list_filter = ("currency", "language", "lesson_type", 'duration')
    search_fields = ("name",)
    list_select_related = ('currency',)

    @admin.display(description=_('Price'))
    def price(self, obj):
        return f"{obj.amount} {obj.currency.code}"