from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveUpdateAPIView

from users.serializers.cabinet.account import AccountCabinetSerializer


@extend_schema(tags=["Cabinet"])
class AccountCabinetView(RetrieveUpdateAPIView):
    """The signed-in user's own account — read identity + role flags, edit
    personal fields (name, phone, timezone)."""

    serializer_class = AccountCabinetSerializer

    def get_object(self):
        return self.request.user
