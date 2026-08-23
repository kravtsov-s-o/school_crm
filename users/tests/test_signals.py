import pytest

from users.models import StudentProfile, TeacherProfile


@pytest.mark.django_db
def test_student_flag_creates_profile(student_user):
    assert StudentProfile.objects.filter(user=student_user).exists()


@pytest.mark.django_db
def test_teacher_flag_creates_profile(teacher_user):
    assert TeacherProfile.objects.filter(user=teacher_user).exists()


@pytest.mark.django_db
def test_no_flags_no_profile(user):
    assert not StudentProfile.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_unsetting_student_flag_deactivates_profile(student_user):
    student_user.is_student = False
    student_user.save()
    profile = StudentProfile.objects.get(user=student_user)
    assert profile.is_active is False


@pytest.mark.django_db
def test_resetting_student_flag_reactivates_profile(student_user):
    student_user.is_student = False
    student_user.save()
    student_user.is_student = True
    student_user.save()
    profile = StudentProfile.objects.get(user=student_user)
    assert profile.is_active is True
