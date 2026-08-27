from rest_framework.routers import DefaultRouter

from users.views.admin.student import StudentViewSet
from users.views.admin.teacher import TeacherViewSet
from users.views.admin.user import UserAdminViewSet

router = DefaultRouter()
router.register("users", UserAdminViewSet, basename="user")
router.register("students", StudentViewSet, basename="student")
router.register("teachers", TeacherViewSet, basename="teacher")

urlpatterns = [
    *router.urls,
]
