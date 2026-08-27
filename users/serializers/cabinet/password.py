from rest_framework import serializers

from users.serializers.common import validate_password_strength


class ChangePasswordSerializer(serializers.Serializer):
    """Old + new password payload for the cabinet change-password action;
    verifies the current password before allowing the change."""

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True,
                                         validators=[validate_password_strength])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect")
        return value
