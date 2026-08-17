from django import forms
from django.utils.translation import gettext_lazy as _

from lessons.models import Lesson


class LessonAdminForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = "__all__"  # noqa: DJ007

    def clean(self):
        cleaned = super().clean()
        lesson_type = cleaned.get("lesson_type")
        students = cleaned.get("students")

        if students:
            currencies = {student.currency_id for student in students}
            if len(currencies) > 1:
                raise forms.ValidationError(
                    {"students": _("All students must have one currency")}
                )

        if lesson_type and students is not None:
            count = len(students)

            if (lesson_type.min_participants is None
                    and lesson_type.max_participants is None and count != 1):
                raise forms.ValidationError(
                    {"students": _("Must be only 1 student.")},
                )

            if lesson_type.min_participants and count < lesson_type.min_participants:
                raise forms.ValidationError(
                    {
                        "students":
                            _("Min students for this lesson type must be {count}.")
                            .format(count=lesson_type.min_participants)
                    },
                )

            if lesson_type.max_participants and count > lesson_type.max_participants:
                raise forms.ValidationError(
                    {
                        "students":
                            _("Max students for this lesson type must be {count}.")
                            .format(count=lesson_type.max_participants)
                    },
                )

        return cleaned
