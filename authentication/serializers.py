from rest_framework import serializers

from users.serializers.common import validate_password_strength


class PasswordResetRequestSerializer(serializers.Serializer):
    """Password-reset request payload — just the email."""

    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Password-reset confirm payload — uid, token, and the new (validated) password."""

    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True,
                                         validators=[
                                             validate_password_strength
                                         ])
