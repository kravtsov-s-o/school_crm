from django.urls import path

from users.views.cabinet.account import AccountView
from users.views.cabinet.student_profile import StudentProfileView

urlpatterns = [
    path("account/", AccountView.as_view(), name="account"),
    path("student-profile/", StudentProfileView.as_view()),
    # path("teacher-profile/", TeacherProfileView.as_view()),
]
