from django.contrib import admin

from companies.models import Company


# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'currency', 'coverage_percent', 'account', 'personal_plan', 'is_active')
    list_filter = ('currency', 'is_active', 'personal_plan')
    search_fields = ('name',)

    readonly_fields = ('account',)
