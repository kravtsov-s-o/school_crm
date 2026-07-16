from django.contrib import admin

from core._helpers import SystemProtectedAdminMixin
from school_settings.models import (
    Currency,
    Duration,
    ExchangeRate,
    Language,
    LessonType,
    TeacherGrade,
)


# Register your models here.
@admin.register(Language)
class LanguageAdmin(SystemProtectedAdminMixin, admin.ModelAdmin):
    list_display = ("name", "is_system", "is_active")
    list_filter = ("is_system", "is_active")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Currency)
class CurrencyAdmin(SystemProtectedAdminMixin, admin.ModelAdmin):
    list_display = ("code", "name", "symbol", "is_system", "is_active")
    list_filter = ("is_system", "is_active")
    search_fields = ("code", "name")
    ordering = ("code",)


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ("currency", "rate", "date")
    list_filter = ("currency", "date")


@admin.register(Duration)
class DurationAdmin(SystemProtectedAdminMixin, admin.ModelAdmin):
    list_display = ("minutes", "is_system", "is_active")
    list_filter = ("is_system", "is_active")
    ordering = ("minutes",)


@admin.register(LessonType)
class LessonTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "min_participants",
        "max_participants",
        "duration_affects_price",
        "is_active",
    )
    list_filter = ("is_active", "duration_affects_price")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(TeacherGrade)
class TeacherGradeAdmin(admin.ModelAdmin):
    list_display = ("name", "sort_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    list_editable = ("sort_order",)
