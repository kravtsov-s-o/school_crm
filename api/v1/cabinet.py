from django.urls import path
from rest_framework.routers import DefaultRouter

from finance.views.cabinet.transaction import (
    StudentTransactionCabinetViewSet,
    TeacherTransactionCabinetViewSet,
)
from lessons.views.cabinet.student_lesson import StudentLessonCabinetViewSet
from lessons.views.cabinet.teacher_lesson import TeacherLessonCabinetViewSet
from users.views.cabinet.account import AccountCabinetView
from users.views.cabinet.password import ChangePasswordView
from users.views.cabinet.student import StudentCabinetView
from users.views.cabinet.teacher import TeacherCabinetView
from users.views.cabinet.teacher_card import TeacherCardCabinetViewSet

router = DefaultRouter()
router.register("student-transactions", StudentTransactionCabinetViewSet,
                basename="student-transaction")
router.register("teacher-transactions", TeacherTransactionCabinetViewSet,
                basename="teacher-transaction")
router.register("student-lessons", StudentLessonCabinetViewSet,
                basename="student-lesson")
router.register("teacher-lessons", TeacherLessonCabinetViewSet,
                basename="teacher-lesson")
router.register("teacher-cards", TeacherCardCabinetViewSet,
                basename="teacher-card")

urlpatterns = [
    path("account/", AccountCabinetView.as_view(), name="account"),
    path("student/", StudentCabinetView.as_view()),
    path("teacher/", TeacherCabinetView.as_view()),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    *router.urls,
]
