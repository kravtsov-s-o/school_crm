from django.contrib import admin

from finance.models import Account, Transaction


# Register your models here.
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    search_fields = (
        "student_profile__user__first_name",
        "student_profile__user__last_name",
        "student_profile__user__email",
        "teacher_profile__user__first_name",
        "teacher_profile__user__last_name",
        "teacher_profile__user__email",
        "company__name",
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("date", "account", "amount", "currency", "lesson", "type")
    list_filter = ("type", "currency", "date")
    list_select_related = ("account", "currency", "lesson")
    autocomplete_fields = ("account", "lesson", "currency")
    search_fields = (
        "account__student_profile__user__first_name",
        "account__student_profile__user__last_name",
        "account__student_profile__user__email",
        "account__teacher_profile__user__first_name",
        "account__teacher_profile__user__last_name",
        "account__teacher_profile__user__email",
        "account__company__name",
    )

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
