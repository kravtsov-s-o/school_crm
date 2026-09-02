from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets

from finance.filters import TransactionFilter
from finance.models import Transaction
from finance.serializers.cabinet.transaction import TransactionCabinetSerializer


@extend_schema(tags=["Cabinet: Student Transactions"])
class StudentTransactionCabinetViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = TransactionCabinetSerializer
    filterset_class = TransactionFilter
    ordering_fields = ("date", "type", "currency__code")

    def get_queryset(self):
        return (Transaction.objects.select_related("currency", "lesson")
                    .filter(account__student_profile__user=self.request.user))


@extend_schema(tags=["Cabinet: Teacher Transactions"])
class TeacherTransactionCabinetViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = TransactionCabinetSerializer
    filterset_class = TransactionFilter
    ordering_fields = ("date", "type", "currency__code")

    def get_queryset(self):
        return (Transaction.objects.select_related("currency", "lesson")
                    .filter(account__teacher_profile__user=self.request.user))
