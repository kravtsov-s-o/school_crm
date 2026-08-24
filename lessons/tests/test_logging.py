import logging

import pytest

from lessons.models import Lesson
from lessons.services import LessonChangeStatus


@pytest.mark.django_db
def test_conduct_logs_transition(lesson, caplog):
    caplog.set_level(logging.INFO)
    LessonChangeStatus(lesson, Lesson.Status.CONDUCTED).apply()
    assert f"lesson {lesson.pk}" in caplog.text
    assert "applied" in caplog.text


@pytest.mark.django_db
def test_no_op_logs_warning(lesson, caplog):
    LessonChangeStatus(lesson, Lesson.Status.CONDUCTED).apply()
    caplog.clear()
    caplog.set_level(logging.WARNING)
    LessonChangeStatus(lesson, Lesson.Status.MISSED).apply()
    assert any(r.levelname == "WARNING" for r in caplog.records)
    assert "no-op" in caplog.text
