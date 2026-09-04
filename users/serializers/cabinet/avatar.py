from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from users.models import User

MAX_AVATAR_SIZE = 2 * 1024 * 1024  # 2MB


def validate_avatar_size(f):
    if f.size > MAX_AVATAR_SIZE:
        raise serializers.ValidationError(_("Avatar size must be ≤ 2 MB."))


class AvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(validators=[
        FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'webp']),
        validate_avatar_size,
    ])

    class Meta:
        model = User
        fields = ('avatar',)
