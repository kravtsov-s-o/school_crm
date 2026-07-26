from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from pricing.models import (
    PersonalPlan,
    PersonalPlanRow,
    SchoolPrice,
    SchoolPriceRow,
    TeacherRate,
    TeacherRateRow,
)


# Register your models here.
class BasePriceRowInline(admin.TabularInline):
    extra = 0
    verbose_name = _("Price Row")
    fields = ("duration", "amount")


class SchoolPriceRowInline(BasePriceRowInline):
    model = SchoolPriceRow


class TeacherRateRowInline(BasePriceRowInline):
    model = TeacherRateRow


class PersonalPlanRowInline(BasePriceRowInline):
    model = PersonalPlanRow


class BasePriceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price_per_hour",
        "currency",
        "language",
        "lesson_type",
        "is_active",
    )
    list_filter = ("currency", "language", "lesson_type")
    search_fields = ("name",)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("rows__duration")

    @admin.display(description=_("Price / hour"))
    def price_per_hour(self, obj):
        for row in obj.rows.all():
            if row.duration.minutes == 60:
                return row.amount
        return "—"


@admin.register(SchoolPrice)
class SchoolPriceAdmin(BasePriceAdmin):
    autocomplete_fields = ("currency", "language")
    inlines = [SchoolPriceRowInline]


@admin.register(TeacherRate)
class TeacherRateAdmin(BasePriceAdmin):
    list_display = (*BasePriceAdmin.list_display, "grade")
    list_filter = (*BasePriceAdmin.list_filter, "grade")
    autocomplete_fields = ("currency", "language")
    inlines = [TeacherRateRowInline]


@admin.register(PersonalPlan)
class PersonalPlanAdmin(BasePriceAdmin):
    autocomplete_fields = ("currency", "language")
    search_fields = ("name",)
    inlines = [PersonalPlanRowInline]
