from django import forms
from django.utils.translation import gettext_lazy as _

from users.models import StudentProfile


class StudentProfileAdminForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = '__all__'  # noqa: DJ007

    def clean(self):
        cleaned = super().clean()
        currency = cleaned.get('currency')
        plans = cleaned.get('personal_plans')

        if currency and plans:
            wrong = [p for p in plans if p.currency_id != currency.id]

            if wrong:
                raise forms.ValidationError({
                    "personal_plans": _("All plans must match the student currency.")
                })

        return cleaned
