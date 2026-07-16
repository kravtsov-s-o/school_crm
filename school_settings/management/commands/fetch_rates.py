from datetime import datetime
from decimal import Decimal

import requests
from django.core.management import BaseCommand, CommandError

from school_settings.models import Currency, ExchangeRate


# Work with command manual
# poetry run python manage.py fetch_rates
class Command(BaseCommand):
    help = "Fetch daily NBU exchange rates"

    def get_currencies(self):
        return Currency.objects.filter(is_active=True, is_system=False)

    def handle(self, *args, **options):
        url = "https://bank.gov.ua/NBU_Exchange/exchange?json"

        currencies = self.get_currencies()

        currency_rates = []

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            by_code = {c.code: c for c in currencies}

            for item in data:
                currency = by_code.get(item["CurrencyCodeL"])
                if not currency:
                    continue

                rate = Decimal(str(item["Amount"])) / item["Units"]
                date = datetime.strptime(item["StartDate"], "%d.%m.%Y").date()  # noqa: DTZ007

                currency_rates.append(
                    ExchangeRate(
                        currency=currency,
                        rate=rate,
                        date=date,
                    )
                )

            ExchangeRate.objects.bulk_create(
                currency_rates,
                update_conflicts=True,
                update_fields=["rate", "updated_at"],
                unique_fields=["currency", "date"],
            )
            self.stdout.write(self.style.SUCCESS(f"Saved {len(currency_rates)} rates"))

        except requests.exceptions.RequestException as e:
            raise CommandError(f"Request error: {e}") from e
