from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from lessons.models import Lesson


# Register your models here.
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "start_at",
        "status",
        "get_students",
        "get_topic",
        "duration",
        "teacher",
        "language",
        "lesson_type",
    )
    list_filter = (
        "status",
        "duration",
        "teacher",
        "language",
        "lesson_type",
        "students",
    )
    search_fields = (
        "teacher__user__first_name",
        "teacher__user__last_name",
        "teacher__user__email",
        "topic",
        "notes",
        "homework",
    )
    readonly_fields = ("lesson_price", "lesson_currency")
    filter_horizontal = ("students",)

    @admin.display(description=_("Students"))
    def get_students(self, obj):
        return ", ".join([str(item) for item in obj.students.all()])

    @admin.display(description=_("Topic"))
    def get_topic(self, obj):
        return obj.topic[:30]
