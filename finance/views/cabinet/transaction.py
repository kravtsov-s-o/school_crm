from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets

from finance.filters import TransactionFilter
from finance.models import Transaction
from finance.serializers.cabinet.transaction import TransactionCabinetSerializer


class BaseTransactionCabinetViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Base cabinet transaction ledger (read-only list, period/type filters);
    subclasses scope to the user's own account."""

    serializer_class = TransactionCabinetSerializer
    filterset_class = TransactionFilter
    ordering_fields = ("date", "type", "currency__code")


@extend_schema(tags=["Cabinet: Student Transactions"])
class StudentTransactionCabinetViewSet(BaseTransactionCabinetViewSet):
    """The signed-in user's own student-account transactions."""

    def get_queryset(self):
        return (Transaction.objects.select_related("currency", "lesson")
                .filter(account__student_profile__user=self.request.user))


@extend_schema(tags=["Cabinet: Teacher Transactions"])
class TeacherTransactionCabinetViewSet(BaseTransactionCabinetViewSet):
    """The signed-in user's own teacher-account transactions."""

    def get_queryset(self):
        return (Transaction.objects.select_related("currency", "lesson")
                .filter(account__teacher_profile__user=self.request.user))
