import pytest


@pytest.mark.django_db
def test_user_delete_is_soft(student_user):
    student_user.delete()
    student_user.refresh_from_db()
    assert student_user.is_active is False
