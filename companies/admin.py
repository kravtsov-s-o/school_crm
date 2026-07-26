from django.contrib import admin
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from companies.forms import CompanyAdminForm
from companies.models import Company


# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "balance",
        "currency",
        "coverage_percent",
        "account",
        "get_personal_plans",
        "is_active",
    )
    list_filter = ("currency", "is_active", "personal_plans")
    search_fields = ("name",)

    readonly_fields = ("account",)
    autocomplete_fields = ("personal_plans", "currency")

    form = CompanyAdminForm

    @admin.display(description=_("Personal Plans"))
    def get_personal_plans(self, obj):
        return ", ".join([str(item) for item in obj.personal_plans.all()])

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            _balance=Sum("account__transactions__amount")
        )

    @admin.display(description=_("Balance"), ordering="_balance")
    def balance(self, obj):
        return obj._balance or 0
