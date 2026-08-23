from decimal import ROUND_HALF_UP, Decimal

from django.db import transaction

from finance.models import TransactionCode
from finance.services import register_transaction
from lessons.models import Lesson
from pricing.services import SeatPriceResolver, TeacherRateResolver


class LessonChangeStatus:
    def __init__(self, lesson, status):
        self.lesson = lesson
        self.status = status

    def apply(self):
        CHARGED = {Lesson.Status.CONDUCTED, Lesson.Status.MISSED}

        with transaction.atomic():
            self.lesson = Lesson.objects.select_for_update().get(pk=self.lesson.pk)
            old = self.lesson.status
            entering = old not in CHARGED and self.status in CHARGED
            leaving = old in CHARGED and self.status not in CHARGED

            self.lesson.status = self.status

            if entering:
                lesson_code = TransactionCode.LESSON_CHARGE
                teacher_code = TransactionCode.TEACHER_ACCRUAL
            elif leaving:
                lesson_code = TransactionCode.LESSON_REFUND
                teacher_code = TransactionCode.TEACHER_REFUND
            else:
                self.lesson.save()
                return

            teacher_price, teacher_currency, _ = self.get_teacher_price()
            register_transaction(
                self.lesson.teacher.account,
                teacher_price,
                teacher_currency,
                teacher_code,
                self.lesson
            )

            total = Decimal("0.00")
            currency = None
            for student in self.lesson.students.all():
                student_part, company_part, currency = self.calc_participant_price(student)
                total += student_part + company_part
                if student_part:
                    register_transaction(
                        student.account,
                        student_part,
                        currency,
                        lesson_code,
                        self.lesson
                    )
                if company_part:
                    register_transaction(
                        student.company.account,
                        company_part,
                        currency,
                        lesson_code,
                        self.lesson
                    )

            self.lesson.lesson_price = total if entering else None
            self.lesson.lesson_currency = currency if entering else None

            self.lesson.save()

    def calc_participant_price(self, student):
        student_price = SeatPriceResolver(
            student,
            self.lesson.language,
            self.lesson.lesson_type,
            self.lesson.duration
        ).resolve()

        if student_price.source == "company":
            company_price = ((student_price.amount * student_price.coverage_percent / 100)
                             .quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
            price = student_price.amount - company_price
        else:
            price = student_price.amount
            company_price = 0

        return price, company_price, student_price.currency

    def get_teacher_price(self):
        teacher = self.lesson.teacher
        teacher_price = TeacherRateResolver(
            self.lesson.language,
            self.lesson.lesson_type,
            teacher.currency,
            self.lesson.duration,
            teacher.grade,
        ).resolve()

        return teacher_price.amount, teacher_price.currency, teacher_price.source


class LessonListChangeStatus:
    def __init__(self, lessons, status):
        self.lessons = lessons
        self.status = status

    def update(self):
        count = 0
        for lesson in self.lessons:
            if lesson.status != self.status:
                LessonChangeStatus(lesson, self.status).apply()
                count += 1

        return count
