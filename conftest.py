from decimal import Decimal

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
def duration_45(db):
    from school_settings.models import Duration
    return Duration.objects.get(minutes=45)


@pytest.fixture
def account(db):
    from finance.models import Account
    return Account.objects.create()


@pytest.fixture
def grade(db):
    from school_settings.models import TeacherGrade
    return TeacherGrade.objects.create(name="Middle")


@pytest.fixture
def student(db, currency_uah):
    from users.models import User
    user = User.objects.create(username="s1", email="s1@x.com", is_student=True)
    profile = user.studentprofile  # сигнал создал профиль
    profile.currency = currency_uah
    profile.save()
    return profile


@pytest.fixture
def plan_usd(currency_usd, language_en, lesson_type_personal, duration_60):
    from pricing.models import PersonalPlan, PersonalPlanRow
    plan = PersonalPlan.objects.create(
        name="Personal USD", currency=currency_usd,
        language=language_en, lesson_type=lesson_type_personal,
    )
    PersonalPlanRow.objects.create(plan=plan, duration=duration_60, amount=Decimal("40"))
    return plan
