from django.db import models
from django.utils.translation import gettext_lazy as _

from core._mixins import TimeStampMixin


# Create your models here.
class Lesson(TimeStampMixin):
    class Status(models.TextChoices):
        PLANNED = "planned", _("Planned")
        CONDUCTED = "conducted", _("Conducted")
        MISSED = "missed", _("Missed")

    teacher = models.ForeignKey(
        "users.TeacherProfile",
        on_delete=models.PROTECT,
        null=True,
        related_name="lessons",
        verbose_name=_("Teacher"),
    )
    language = models.ForeignKey(
        "school_settings.Language",
        on_delete=models.PROTECT,
        null=True,
        verbose_name=_("Language"),
    )
    lesson_type = models.ForeignKey(
        "school_settings.LessonType",
        on_delete=models.PROTECT,
        null=True,
        verbose_name=_("LessonType"),
    )
    status = models.CharField(
        default=Status.PLANNED,
        choices=Status.choices,
        max_length=10,
        verbose_name=_("Status"),
    )
    start_at = models.DateTimeField(verbose_name=_("Start at"))
    duration = models.ForeignKey(
        "school_settings.Duration",
        on_delete=models.PROTECT,
        null=True,
        verbose_name=_("Duration"),
    )
    students = models.ManyToManyField(
        "users.StudentProfile", related_name="lessons", verbose_name=_("Students")
    )
    meeting_url = models.URLField(
        max_length=255, blank=True, verbose_name=_("Meeting URL")
    )
    topic = models.CharField(max_length=255, verbose_name=_("Topic"))
    notes = models.TextField(blank=True, verbose_name=_("Notes"))
    homework = models.TextField(blank=True, verbose_name=_("Homework"))
    lesson_price = models.DecimalField(
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Lesson price"),
    )
    lesson_currency = models.ForeignKey(
        "school_settings.Currency",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("Currency"),
    )

    def __str__(self):
        return f"{self.topic[:10]}"

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = _("Lesson")
        verbose_name_plural = _("Lessons")
        ordering = ("-start_at",)
