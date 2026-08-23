import pytest
from django.core.exceptions import ValidationError

from companies.models import Company
from users.forms import StudentProfileAdminForm


@pytest.mark.django_db
def test_student_company_currency_mismatch(student, currency_usd):
    company_usd = Company.objects.create(name="ACME", currency=currency_usd)
    student.company = company_usd
    with pytest.raises(ValidationError):
        student.clean()


@pytest.mark.django_db
def test_student_company_currency_match_ok(student, currency_uah):
    company_uah = Company.objects.create(name="ACME", currency=currency_uah)
    student.company = company_uah
    student.clean()


@pytest.mark.django_db
def test_student_form_rejects_plan_currency_mismatch(currency_uah, plan_usd):
    form = StudentProfileAdminForm(data={
        "currency": currency_uah.pk,
        "personal_plans": [plan_usd.pk],
    })
    form.is_valid()
    assert "personal_plans" in form.errors


@pytest.mark.django_db
def test_student_form_rejects_plan_currency_match(currency_usd, plan_usd):
    form = StudentProfileAdminForm(data={
        "currency": currency_usd.pk,
        "personal_plans": [plan_usd.pk],
    })
    form.is_valid()
    assert "personal_plans" not in form.errors
