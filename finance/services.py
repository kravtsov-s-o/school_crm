def signed_amount(amount, code):
    from finance.models import TransactionCode

    amount = abs(amount)
    if TransactionCode(code).direction == "expense":
        amount = -amount
    return amount


def register_transaction(account, amount, currency, code, lesson=None, comment=""):
    """
    Register transaction
    :param account:
    :param amount:
    :param currency:
    :param code:
    :param lesson:
    :param comment:
    :return: Transaction
    """
    from finance.models import Transaction

    return Transaction.objects.create(
        account=account,
        amount=amount,
        currency=currency,
        type=code,
        lesson=lesson,
        comment=comment
    )
