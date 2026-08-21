import pytest


@pytest.fixture
def currency_uah(db):
    from school_settings.models import Currency
    return Currency.objects.get(code="UAH")


@pytest.fixture
def currency_usd(db):
    from school_settings.models import Currency
    return Currency.objects.get(code="USD")


@pytest.fixture
def language_en(db):
    from school_settings.models import Language
    return Language.objects.get(name="English")


@pytest.fixture
def lesson_type_personal(db):
    from school_settings.models import LessonType
    return LessonType.objects.get(name="Personal")


@pytest.fixture
def duration_60(db):
    from school_settings.models import Duration
    return Duration.objects.get(minutes=60)


@pytest.fixture
def account(db):
    from finance.models import Account
    return Account.objects.create()