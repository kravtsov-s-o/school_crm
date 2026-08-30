import django_filters

from lessons.models import Lesson


class LessonFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name="start_at", lookup_expr="date")
    date_from = django_filters.DateFilter(field_name="start_at", lookup_expr="date__gte")
    date_to = django_filters.DateFilter(field_name="start_at", lookup_expr="date__lte")

    class Meta:
        model = Lesson
        fields = ("status", "teacher", "language", "lesson_type", "date", "date_from", "date_to")
