from decimal import Decimal

import pytest

from companies.models import Company
from pricing.services import (
    PriceNotFound,
    SchoolPriceResolver,
    SeatPriceResolver,
    TeacherRateResolver,
)
from school_settings.models import TeacherGrade


@pytest.mark.django_db
def test_school_resolver_returns_price(
        school_price,
        language_en,
        lesson_type_personal,
        currency_uah,
        duration_60
):
    resolved = SchoolPriceResolver(
        language_en,
        lesson_type_personal,
        currency_uah,
        duration_60
    ).resolve()
    assert resolved.amount == Decimal(500)
    assert resolved.source == "school"


@pytest.mark.django_db
def test_school_resolver_no_plan_raises(
        language_en,
        lesson_type_personal,
        currency_uah,
        duration_60
):
    with pytest.raises(PriceNotFound):
        SchoolPriceResolver(
            language_en,
            lesson_type_personal,
            currency_uah,
            duration_60
        ).resolve()


@pytest.mark.django_db
def test_school_resolver_no_duration_raises(
        school_price,
        language_en,
        lesson_type_personal,
        currency_uah,
        duration_45
):
    with pytest.raises(PriceNotFound):
        SchoolPriceResolver(
            language_en,
            lesson_type_personal,
            currency_uah,
            duration_45
        ).resolve()


@pytest.mark.django_db
def test_teacher_rate_returns_price(
        teacher_rate,
        language_en,
        lesson_type_personal,
        currency_uah,
        duration_60,
        grade
):
    resolved = TeacherRateResolver(
        language_en,
        lesson_type_personal,
        currency_uah,
        duration_60,
        grade
    ).resolve()
    assert resolved.amount == Decimal(300)
    assert resolved.source == "teacher"


@pytest.mark.django_db
def test_teacher_rate_wrong_grade_raises(
        teacher_rate,
        language_en,
        lesson_type_personal,
        currency_uah,
        duration_60
):
    other_grade = TeacherGrade.objects.create(name="Senior")
    with pytest.raises(PriceNotFound):
        TeacherRateResolver(
            language_en,
            lesson_type_personal,
            currency_uah,
            duration_60,
            other_grade
        ).resolve()


@pytest.mark.django_db
def test_seat_falls_to_school(
        student,
        school_price,
        language_en,
        lesson_type_personal,
        duration_60
):
    resolved = SeatPriceResolver(
        student,
        language_en,
        lesson_type_personal,
        duration_60
    ).resolve()
    assert resolved.amount == Decimal(500)
    assert resolved.source == "school"
    assert resolved.coverage_percent is None


@pytest.mark.django_db
def test_seat_uses_personal_plan(
        student,
        personal_plan,
        school_price,
        language_en,
        lesson_type_personal,
        duration_60
):
    student.personal_plans.add(personal_plan)
    resolved = SeatPriceResolver(
        student,
        language_en,
        lesson_type_personal,
        duration_60
    ).resolve()
    assert resolved.amount == Decimal(400)
    assert resolved.source == "personal"
    assert resolved.coverage_percent is None


@pytest.fixture
def company(currency_uah, personal_plan):
    company = Company.objects.create(name="ACME", currency=currency_uah, coverage_percent=50)
    company.personal_plans.add(personal_plan)
    return company


@pytest.mark.django_db
def test_seat_uses_company_plan(
        student,
        company,
        school_price,
        language_en,
        lesson_type_personal,
        duration_60
):
    student.company = company
    student.save()
    resolved = SeatPriceResolver(
        student,
        language_en,
        lesson_type_personal,
        duration_60
    ).resolve()
    assert resolved.amount == Decimal(400)
    assert resolved.source == "company"
    assert resolved.coverage_percent == 50


@pytest.mark.django_db
def test_company_beats_personal(
        student,
        company,
        personal_plan,
        language_en,
        lesson_type_personal,
        duration_60
):
    student.company = company
    student.save()
    student.personal_plans.add(personal_plan)
    resolved = SeatPriceResolver(student, language_en, lesson_type_personal, duration_60).resolve()
    assert resolved.source == "company"
    assert resolved.coverage_percent == 50
