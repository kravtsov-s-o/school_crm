from django import forms
from django.utils.translation import gettext_lazy as _
from nh3 import nh3

from core.widgets.quill_admin_widget import QuillAdminWidget
from users.models import StudentProfile, TeacherProfile


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


class TeacherProfileAdminForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = '__all__'
        widgets = {"about_me": QuillAdminWidget()}

    def clean_about_me(self):
        return nh3.clean(self.cleaned_data.get("about_me", ""))
