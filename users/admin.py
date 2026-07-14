from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from users.models import User, Student, StudentProfile, TeacherProfile, Teacher

ADDITIONAL_FIELDSET = (
    _("Additional Fields"),
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
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        ADDITIONAL_FIELDSET,
    )
    fieldsets = DjangoUserAdmin.fieldsets + (ADDITIONAL_FIELDSET,)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in instances:
            if not obj.pk:
                existing = type(obj).objects.filter(user=form.instance).first()
                if existing:
                    obj.pk = existing.pk
            obj.save()
        formset.save_m2m()


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
