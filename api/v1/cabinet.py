from django.urls import path

from users.views.cabinet.account import AccountCabinetView
from users.views.cabinet.password import ChangePasswordView
from users.views.cabinet.student import StudentCabinetView
from users.views.cabinet.teacher import TeacherCabinetView

urlpatterns = [
    path("account/", AccountCabinetView.as_view(), name="account"),
    path("student/", StudentCabinetView.as_view()),
    path("teacher/", TeacherCabinetView.as_view()),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
]
