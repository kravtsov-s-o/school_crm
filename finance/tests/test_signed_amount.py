from decimal import Decimal

from finance.models import TransactionCode
from finance.services import signed_amount


def test_expense_in_negative():
    assert signed_amount(Decimal(100), TransactionCode.LESSON_CHARGE) == Decimal(-100)


def test_expense_in_positive():
    assert signed_amount(Decimal(100), TransactionCode.MANUAL_TOPUP) == Decimal(100)


def test_sign_ignores_input_sign():
    assert signed_amount(Decimal(-100), TransactionCode.MANUAL_TOPUP) == Decimal(100)
