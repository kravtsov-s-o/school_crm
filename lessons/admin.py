from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

from lessons.forms import LessonAdminForm
from lessons.models import Lesson
from lessons.services import LessonListChangeStatus


# Register your models here.
def change_lesson_status_action(status, message_level):
    def action(modeladmin, request, queryset):
        lessons_to_change = LessonListChangeStatus(queryset, status)
        count = lessons_to_change.update()
        messages.add_message(
            request,
            message_level,
            _("{count} Lessons successfully changed to {status}")
            .format(count=count, status=status.capitalize()),
        )

    action.__name__ = f"make_{status.lower()}"
    return admin.action(description=_("Mark lesson status as '{status}")
                        .format(status=status.capitalize()))(action)


make_conducted = change_lesson_status_action(Lesson.Status.CONDUCTED, messages.SUCCESS)
make_planned = change_lesson_status_action(Lesson.Status.PLANNED, messages.SUCCESS)
make_missed = change_lesson_status_action(Lesson.Status.MISSED, messages.SUCCESS)


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
        "lesson_price",
        "lesson_currency"
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
    autocomplete_fields = ("students", "teacher", "language", "duration")
    form = LessonAdminForm

    def get_queryset(self, request):
        return (super().get_queryset(request)
                .select_related("lesson_type", "teacher")
                .prefetch_related("students__user"))

    @admin.display(description=_("Students"))
    def get_students(self, obj):
        return ", ".join([str(item) for item in obj.students.all()])

    @admin.display(description=_("Topic"))
    def get_topic(self, obj):
        return obj.topic[:30]

    actions = [make_conducted, make_planned, make_missed]
