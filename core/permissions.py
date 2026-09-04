from rest_framework import permissions


class IsTeacherUser(permissions.BasePermission):
    """Allows only users with the ``is_teacher`` flag (safe for AnonymousUser)."""

    def has_permission(self, request, view):
        return getattr(request.user, "is_teacher", False)
