from django.contrib import admin

from core._helpers import SystemProtectedAdminMixin
from finance.models import TransactionType, Transaction, Account


# Register your models here.
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    search_fields = (
        'student_profile__user__first_name',
        'student_profile__user__last_name',
        'student_profile__user__email',
        'teacher_profile__user__first_name',
        'teacher_profile__user__last_name',
        'teacher_profile__user__email',
        'company__name',
    )


@admin.register(TransactionType)
class TransactionTypeAdmin(SystemProtectedAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'code', 'direction', 'is_active', 'is_system')
    list_filter = ('direction', 'is_system')
    search_fields = ('name', 'code')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'account', 'amount', 'currency', 'lesson', 'type')
    list_filter = ('type', 'currency', 'date')
    list_select_related = ('account', 'currency', 'type', 'lesson')
    autocomplete_fields = ('account', 'lesson')

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False