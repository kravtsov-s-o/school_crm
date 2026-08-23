import pytest

from users.models import Student, Teacher


@pytest.mark.django_db
def test_student_manager_includes_student(student_user):
    assert Student.objects.filter(pk=student_user.pk).exists()


@pytest.mark.django_db
def test_student_manager_excludes_non_student(user):
    assert not Student.objects.filter(pk=user.pk).exists()


@pytest.mark.django_db
def test_student_manager_excludes_inactive(student_user):
    student_user.is_active = False
    student_user.save()
    assert not Student.objects.filter(pk=student_user.pk).exists()


@pytest.mark.django_db
def test_teacher_manager_excludes_inactive(teacher_user):
    teacher_user.is_active = False
    teacher_user.save()
    assert not Teacher.objects.filter(pk=teacher_user.pk).exists()
