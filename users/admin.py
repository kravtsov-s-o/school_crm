from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from users.forms import StudentProfileAdminForm
from users.models import Student, StudentProfile, Teacher, TeacherProfile, User

ADDITIONAL_FIELDSET = (
    _("Additional Fields"),
    {"fields": ("avatar", "timezone", "is_teacher", "is_student", "phone")},
)


# Register your models here.
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
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
    add_fieldsets = (
        *DjangoUserAdmin.add_fieldsets,
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        ADDITIONAL_FIELDSET,
    )
    fieldsets = (*DjangoUserAdmin.fieldsets, ADDITIONAL_FIELDSET)

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
    form = StudentProfileAdminForm
    can_delete = False
    min_num = 1
    max_num = 1

    readonly_fields = ("account",)
    autocomplete_fields = (
        "teacher",
        "languages",
        "currency",
        "company",
        "personal_plans",
    )


@admin.register(Student)
class StudentAdmin(UserAdmin):
    inlines = (StudentProfileInline,)


class TeacherProfileInline(admin.StackedInline):
    model = TeacherProfile
    can_delete = False
    min_num = 1
    max_num = 1

    readonly_fields = ("account",)
    autocomplete_fields = ("languages", "currency", "lesson_types")


@admin.register(Teacher)
class TeacherAdmin(UserAdmin):
    inlines = (TeacherProfileInline,)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    search_fields = ("user__first_name", "user__last_name", "user__email")

    def has_module_permission(self, request):
        return False


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    search_fields = ("user__first_name", "user__last_name", "user__email")

    def has_module_permission(self, request):
        return False
