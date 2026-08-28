from rest_framework.routers import DefaultRouter

from companies.views.admin.company import CompanyAdminViewSet
from finance.views.admin.account import AccountAdminViewSet
from finance.views.admin.transaction import TransactionAdminViewSet
from pricing.views.admin.price import (
    PersonalPlanAdminViewSet,
    SchoolPriceAdminViewSet,
    TeacherRateAdminViewSet,
)
from school_settings.views.admin.currency import CurrencyAdminViewSet
from school_settings.views.admin.duration import DurationAdminViewSet
from school_settings.views.admin.exchange_rate import ExchangeRateAdminViewSet
from school_settings.views.admin.language import LanguageAdminViewSet
from school_settings.views.admin.lesson_type import LessonTypeAdminViewSet
from school_settings.views.admin.teacher_grade import TeacherGradeAdminViewSet
from users.views.admin.student import StudentViewSet
from users.views.admin.teacher import TeacherViewSet
from users.views.admin.user import UserAdminViewSet

router = DefaultRouter()
router.register("users", UserAdminViewSet, basename="user")
router.register("students", StudentViewSet, basename="student")
router.register("teachers", TeacherViewSet, basename="teacher")

router.register("languages", LanguageAdminViewSet, basename="language")
router.register("currencies", CurrencyAdminViewSet, basename="currency")
router.register("exchange-rates", ExchangeRateAdminViewSet, basename="exchange-rate")
router.register("durations", DurationAdminViewSet, basename="duration")
router.register("lesson-types", LessonTypeAdminViewSet, basename="lesson-type")
router.register("teacher-grades", TeacherGradeAdminViewSet, basename="teacher-grade")

router.register("companies", CompanyAdminViewSet, basename="company")

router.register("school-prices", SchoolPriceAdminViewSet, basename="school-price")
router.register("teacher-rates", TeacherRateAdminViewSet, basename="teacher-rate")
router.register("personal-plans", PersonalPlanAdminViewSet, basename="personal-plan")

router.register("accounts", AccountAdminViewSet, basename="account")
router.register("transactions", TransactionAdminViewSet, basename="transaction")

urlpatterns = [
    *router.urls,
]
