from datetime import date
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from school_settings.models import Language, Currency, LessonType, ExchangeRate, Duration


@pytest.mark.django_db
def test_seed_created_system_records():
    assert Currency.objects.filter(code__in=["UAH", "USD", "EUR"]).count() == 3
    assert Currency.objects.get(code="UAH").is_system is True
    assert Language.objects.filter(name="English").exists()
    assert Duration.objects.filter(minutes=60).exists()
    assert LessonType.objects.exists()


@pytest.mark.django_db
def test_is_system_cannot_be_changed():
    lang = Language.objects.create(name="Testish")
    lang.is_system = True
    with pytest.raises(ValidationError):
        lang.save()


@pytest.mark.django_db
def test_is_system_cannot_be_deleted(currency_uah):
    with pytest.raises(ValidationError):
        currency_uah.delete()


@pytest.mark.django_db
def test_non_system_record_can_be_deleted():
    lang = Language.objects.create(name="Testish")
    lang.delete()
    assert not Language.objects.filter(name="Testish").exists()


@pytest.mark.django_db
def test_bulk_delete_blocks_system_record(currency_uah):
    with pytest.raises(ValidationError):
        Currency.objects.filter(code="UAH").delete()


@pytest.mark.django_db
def test_bulk_delete_allows_non_system():
    Language.objects.create(name="Testish")
    Language.objects.filter(name="Testish").delete()
    assert not Language.objects.filter(name="Testish").exists()


@pytest.mark.django_db
def test_max_participants_less_than_min_rejected():
    with pytest.raises(IntegrityError):
        LessonType.objects.create(
            name="Broken", min_participants=5, max_participants=2,
        )


@pytest.mark.django_db
def test_duplicate_rate_per_currency_date_rejected(currency_uah):
    ExchangeRate.objects.create(currency=currency_uah, rate=Decimal("1"), date=date(2026, 1, 1))
    with pytest.raises(IntegrityError):
        ExchangeRate.objects.create(currency=currency_uah, rate=Decimal("2"), date=date(2026, 1, 1))


@pytest.mark.django_db
def test_second_system_currency_rejected():
    with pytest.raises(IntegrityError):
        Currency.objects.create(code="XXX", name="Extra", is_system=True)
