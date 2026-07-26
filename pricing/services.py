from pricing.models import SchoolPrice, SchoolPriceRow, TeacherRate, TeacherRateRow


class SchoolPriceResolver:
    def __init__(self, language, lesson_type, duration, currency, **kwargs):
        self.language = language
        self.lesson_type = lesson_type
        self.duration = duration
        self.currency = currency
        self.owner = None

    def get_owner(self, **kwargs):
        if kwargs['student']:
            self.owner = ('student', kwargs['student'])
        elif kwargs['teacher']:
            self.owner = ('teacher', kwargs['teacher'])

    def resolve(self):
        if self.owner[0] == 'student':
            school_price = SchoolPrice.objects.filter(
                language=self.language,
                lesson_type=self.lesson_type,
                currency=self.currency,
            )

            price = SchoolPriceRow.objects.get(plan=school_price, duration=self.duration)
        elif self.owner[0] == 'teacher':
            teacher_rate = TeacherRate.objects.filter(
                language=self.language,
                lesson_type=self.lesson_type,
                currency=self.currency,
            )

            price = TeacherRateRow.objects.get(plan=teacher_rate, duration=self.duration)

        return price
