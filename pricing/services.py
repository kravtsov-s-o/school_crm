from dataclasses import dataclass
from decimal import Decimal

from pricing.models import SchoolPrice, TeacherRate


class PriceNotFound(Exception):
    """Raised when no price matches the requested key. There is no default price."""


@dataclass
class ResolvedPrice:
    """Outcome of price resolution: the amount, its currency, which tier produced
    it (``source``), and the company coverage percent (set only when it came from
    a company tariff, otherwise ``None``)."""

    amount: Decimal
    currency: object
    source: str
    coverage_percent: int | None = None


class BasePriceResolver:
    """Abstract resolver: find a price plan by key, then its row by duration.
    Subclasses set ``model`` and ``source`` and may extend ``get_plan_filter``."""

    model = None
    source = None

    def __init__(self, language, lesson_type, currency, duration):
        self.language = language
        self.lesson_type = lesson_type
        self.currency = currency
        self.duration = duration

    def get_plan_filter(self):
        return {
            "language": self.language,
            "lesson_type": self.lesson_type,
            "currency": self.currency,
            "is_active": True,
        }

    def resolve(self) -> ResolvedPrice:
        plan = self.model.objects.filter(**self.get_plan_filter()).first()
        if not plan:
            raise PriceNotFound("no plan for this key")
        row = plan.rows.filter(duration=self.duration).first()
        if not row:
            raise PriceNotFound(f"plan has no row for this duration ({self.duration})")
        return ResolvedPrice(row.amount, self.currency, self.source)


class SchoolPriceResolver(BasePriceResolver):
    """Resolves the school base price grid. The fallback tier for a student."""

    model = SchoolPrice
    source = "school"


class TeacherRateResolver(BasePriceResolver):
    """Resolves a teacher's pay rate. Keyed additionally by grade."""

    model = TeacherRate
    source = "teacher"

    def __init__(self, language, lesson_type, currency, duration, grade):
        super().__init__(language, lesson_type, currency, duration)
        self.grade = grade

    def get_plan_filter(self):
        return {**super().get_plan_filter(), "grade": self.grade}


class SeatPriceResolver(SchoolPriceResolver):
    """Resolves the full seat price for a student's lesson, in priority order:
    company tariff -> personal plan -> school grid. Payer-neutral: the company/
    student split is applied downstream from ``source``/``coverage_percent``."""

    def __init__(self, student, language, lesson_type, duration):
        super().__init__(language, lesson_type, student.currency, duration)
        self.student = student

    def resolve(self) -> ResolvedPrice:
        return self._from_company() or self._from_personal() or super().resolve()

    def _from_company(self):
        if not self.student.company_id:
            return None

        plan = self.student.company.personal_plans.filter(
            language=self.language,
            lesson_type=self.lesson_type,
            currency=self.currency,
        ).first()
        if not plan:
            return None
        row = plan.rows.filter(duration=self.duration).first()
        return ResolvedPrice(
            row.amount,
            self.currency,
            "company",
            coverage_percent=self.student.company.coverage_percent
        ) if row else None

    def _from_personal(self):
        plan = self.student.personal_plans.filter(
            language=self.language,
            lesson_type=self.lesson_type,
            currency=self.currency,
        ).first()
        if not plan:
            return None
        row = plan.rows.filter(duration=self.duration).first()
        return ResolvedPrice(row.amount, self.currency, "personal") if row else None
