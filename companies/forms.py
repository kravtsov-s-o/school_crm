from django import forms
from django.utils.translation import gettext_lazy as _

from companies.models import Company


class CompanyAdminForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"  # noqa: DJ007

    def clean(self):
        cleaned = super().clean()
        currency = cleaned.get("currency")
        plans = cleaned.get("personal_plans")

        if currency and plans:
            wrong = [p for p in plans if p.currency_id != currency.id]

            if wrong:
                raise forms.ValidationError({
                    "personal_plans": _("All plans must match the company currency.")
                })

        return cleaned
