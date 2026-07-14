import timezone_field
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    avatar = models.ImageField(
        upload_to="avatars/",
        null=True,
        blank=True,
        verbose_name=_("Avatar"),
    )
    timezone = timezone_field.TimeZoneField(
        default=settings.TIME_ZONE,
        verbose_name=_("Timezone")
    )
    is_student = models.BooleanField(default=False, verbose_name=_("Student"))
    is_teacher = models.BooleanField(default=False, verbose_name=_("Teacher"))
    phone = PhoneNumberField(
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("Phone"))
    telegram_id = models.BigIntegerField(
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("Telegram ID")
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return f"{self.email}"

    def __repr__(self):
        return self.__str__()

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save(update_fields=["is_active"])

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ("first_name", "last_name")


class TeacherManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_teacher=True, is_active=True)


class StudentManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_student=True, is_active=True)


class Teacher(User):
    objects = TeacherManager()

    class Meta:
        proxy = True
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")
        ordering = ("first_name", "last_name")


class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True
        verbose_name = _("Student")
        verbose_name_plural = _("Students")
        ordering = ("first_name", "last_name")


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience_since = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name=_("Experience Since"),
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2100),
        ]
    )
    about_me = models.TextField(blank=True, verbose_name=_("About Me"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))

    def __str__(self):
        if self.user.first_name or self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        else:
            return f"{self.user.email}"

    def __repr__(self):
        return self.__str__()


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher = models.ForeignKey(TeacherProfile, null=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))

    def __str__(self):
        if self.user.first_name or self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        else:
            return f"{self.user.email}"

    def __repr__(self):
        return self.__str__()
