from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from finance.models import Transaction, TransactionCode
from finance.services import register_transaction


@pytest.fixture
def topup(account, currency_uah):
    return Transaction.objects.create(
        account=account,
        type=TransactionCode.MANUAL_TOPUP,
        amount=Decimal(100),
        currency=currency_uah,
    )


@pytest.mark.django_db
def test_save_normalizes_expense_to_negative(account, currency_uah):
    txn = Transaction.objects.create(
        account=account,
        type=TransactionCode.LESSON_CHARGE,
        amount=Decimal(100),
        currency=currency_uah,
    )
    assert txn.amount == Decimal(-100)


@pytest.mark.django_db
def test_save_keeps_income_positive(topup):
    assert topup.amount == Decimal(100)


@pytest.mark.django_db
def test_transaction_cannot_be_edited(topup):
    topup.amount = Decimal(200)
    with pytest.raises(ValidationError):
        topup.save()


@pytest.mark.django_db
def test_transaction_cannot_be_deleted(topup):
    with pytest.raises(ValidationError):
        topup.delete()


@pytest.mark.django_db
def test_account_balance_empty_is_zero(account):
    assert account.balance == 0


@pytest.mark.django_db
def test_account_balance_sums_transactions(account, currency_uah):
    Transaction.objects.create(
        account=account, type=TransactionCode.MANUAL_TOPUP,
        amount=Decimal(100), currency=currency_uah,
    )
    Transaction.objects.create(
        account=account, type=TransactionCode.LESSON_CHARGE,
        amount=Decimal(30), currency=currency_uah,
    )
    assert account.balance == Decimal(70)


@pytest.mark.django_db
def test_register_transaction_creates_signed(account, currency_uah):
    txn = register_transaction(
        account, Decimal(100),
        currency_uah, TransactionCode.LESSON_CHARGE
    )

    assert txn.pk is not None
    assert txn.amount == Decimal(-100)
    assert txn.type == TransactionCode.LESSON_CHARGE
    assert txn.account == account


@pytest.mark.django_db
def test_bulk_update_blocked(topup):
    with pytest.raises(ValidationError):
        Transaction.objects.filter(pk=topup.pk).update(amount=Decimal(999))


@pytest.mark.django_db
def test_bulk_delete_blocked(topup):
    with pytest.raises(ValidationError):
        Transaction.objects.filter(pk=topup.pk).delete()
