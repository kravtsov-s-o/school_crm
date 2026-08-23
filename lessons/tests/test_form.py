import pytest

from lessons.forms import LessonAdminForm
from users.models import User


@pytest.mark.django_db
def test_form_rejects_mixed_currencies(student, currency_usd, lesson_type_group):
    other = User.objects.create(username="s2", email="s2@x.com", is_student=True)
    op = other.studentprofile
    op.currency = currency_usd
    op.save()

    form = LessonAdminForm(data={
        "lesson_type": lesson_type_group.pk,
        "students": [student.pk, op.pk],
    })
    form.is_valid()
    assert "students" in form.errors


@pytest.mark.django_db
def test_form_individual_requires_one_student(student, currency_uah, lesson_type_personal):
    other = User.objects.create(username="s2", email="s2@x.com", is_student=True)
    op = other.studentprofile
    op.currency = currency_uah
    op.save()

    form = LessonAdminForm(data={
        "lesson_type": lesson_type_personal.pk,
        "students": [student.pk, op.pk],
    })
    form.is_valid()
    assert "students" in form.errors