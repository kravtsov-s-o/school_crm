from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from users.serializers.cabinet.avatar import AvatarSerializer


@extend_schema(tags=["Cabinet: Avatar"])
class AvatarCabinetView(generics.UpdateAPIView):
    serializer_class = AvatarSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.avatar.delete(save=True)
        return Response(status=status.HTTP_204_NO_CONTENT)
