from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from users.models import User, Student, StudentProfile, TeacherProfile, Teacher

ADDITIONAL_FIELDSET = (
    "Additional Fields",
    {"fields": ("avatar", "timezone", "is_teacher", "is_student", "phone")},
)


# Register your models here.
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'is_staff',
        'is_superuser',
    )
    list_filter = (
        "is_teacher",
        "is_student",
        "is_active",
        "is_superuser",
    )
    search_fields = (
        "email",
        "username",
        "first_name",
        "last_name",
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (ADDITIONAL_FIELDSET,)
    fieldsets = DjangoUserAdmin.fieldsets + (ADDITIONAL_FIELDSET,)


class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    min_num = 1
    max_num = 1


@admin.register(Student)
class StudentAdmin(UserAdmin):
    inlines = (StudentProfileInline,)


class TeacherProfileInline(admin.StackedInline):
    model = TeacherProfile
    can_delete = False
    min_num = 1
    max_num = 1


@admin.register(Teacher)
class TeacherAdmin(UserAdmin):
    inlines = (TeacherProfileInline,)
