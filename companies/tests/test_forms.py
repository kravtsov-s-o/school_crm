import pytest

from companies.forms import CompanyAdminForm


@pytest.mark.django_db
def test_form_rejects_currency_mismatch(currency_uah, plan_usd):
    form = CompanyAdminForm(data={
        "name": "ACME",
        "currency": currency_uah.pk,
        "personal_plans": [plan_usd.pk],
        "coverage_percent": 100,
    })
    assert not form.is_valid()
    assert "personal_plans" in form.errors


@pytest.mark.django_db
def test_form_accepts_matching_currency(currency_usd, plan_usd):
    form = CompanyAdminForm(data={
        "name": "ACME",
        "currency": currency_usd.pk,
        "personal_plans": [plan_usd.pk],
        "coverage_percent": 100,
    })
    assert form.is_valid(), form.errors
