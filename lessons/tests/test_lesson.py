from decimal import Decimal

import pytest

from companies.models import Company
from finance.models import Transaction, TransactionCode
from lessons.models import Lesson
from lessons.services import LessonChangeStatus


@pytest.mark.django_db
def test_conduct_charges_student(lesson, student):
    LessonChangeStatus(lesson, Lesson.Status.CONDUCTED).apply()
    charges = Transaction.objects.filter(
        account=student.account,
        type=TransactionCode.LESSON_CHARGE
    )
    assert charges.count() == 1
    assert charges.first().amount == Decimal(-500)


@pytest.mark.django_db
def test_conduct_accrues_teacher(lesson, teacher):
    LessonChangeStatus(lesson, Lesson.Status.CONDUCTED).apply()
    accruals = Transaction.objects.filter(
        account=teacher.account,
        type=TransactionCode.TEACHER_ACCRUAL
    )
    assert accruals.count() == 1
    assert accruals.first().amount == Decimal(300)


@pytest.mark.django_db
def test_conduct_freezes_lesson_price(lesson):
    LessonChangeStatus(lesson, Lesson.Status.CONDUCTED).apply()
    lesson.refresh_from_db()
    assert lesson.lesson_price == Decimal(500)
    assert lesson.status == Lesson.Status.CONDUCTED


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("coverage", "student_amount", "company_amount"), [
    (0, Decimal(-400), None),
    (50, Decimal(-200), Decimal(-200)),
    (100, None, Decimal(-400)),
])
def test_conduct_splits_coverage(lesson, student, personal_plan, currency_uah,
                                 coverage, student_amount, company_amount):
    company = Company.objects.create(
        name="ACME",
        currency=currency_uah,
        coverage_percent=coverage
    )
    company.personal_plans.add(personal_plan)
    student.company = company
    student.save()

    LessonChangeStatus(lesson, Lesson.Status.CONDUCTED).apply()

    student_q = Transaction.objects.filter(
        account=student.account,
        type=TransactionCode.LESSON_CHARGE
    )
    company_q = Transaction.objects.filter(
        account=company.account,
        type=TransactionCode.LESSON_CHARGE
    )

    if student_amount is None:
        assert not student_q.exists()
    else:
        assert student_q.get().amount == student_amount

    if company_amount is None:
        assert not company_q.exists()
    else:
        assert company_q.get().amount == company_amount


@pytest.mark.django_db
def test_revert_nets_to_zero(lesson, student, teacher):
    LessonChangeStatus(lesson, Lesson.Status.CONDUCTED).apply()
    LessonChangeStatus(lesson, Lesson.Status.PLANNED).apply()

    assert student.account.balance == 0
    assert teacher.account.balance == 0
    lesson.refresh_from_db()
    assert lesson.lesson_price is None
    assert lesson.status == Lesson.Status.PLANNED


@pytest.mark.django_db
def test_conducted_to_missed_no_new_transactions(lesson):
    LessonChangeStatus(lesson, Lesson.Status.CONDUCTED).apply()
    before = Transaction.objects.count()
    LessonChangeStatus(lesson, Lesson.Status.MISSED).apply()
    assert Transaction.objects.count() == before


@pytest.mark.django_db
def test_lesson_price_sums_all_charges(lesson, student, personal_plan, currency_uah):
    company = Company.objects.create(name="ACME", currency=currency_uah, coverage_percent=50)
    company.personal_plans.add(personal_plan)
    student.company = company
    student.save()

    LessonChangeStatus(lesson, Lesson.Status.CONDUCTED).apply()

    lesson.refresh_from_db()
    assert lesson.lesson_price == Decimal(400)
