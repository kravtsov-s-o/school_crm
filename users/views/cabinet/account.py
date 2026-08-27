from rest_framework.generics import RetrieveAPIView

from users.serializers.cabinet.account import AccountSerializer


class AccountView(RetrieveAPIView):
    serializer_class = AccountSerializer

    def get_object(self):
        return self.request.user
