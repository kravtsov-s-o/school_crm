import contextvars
import logging

_current_user = contextvars.ContextVar("current_user", default="anonymous")


def set_current_user(user):
    _current_user.set(user)


class CurrentUserFilter(logging.Filter):
    """Injects the current user (from CurrentUserMiddleware's contextvar)
        into every log record as `record.user`."""

    def filter(self, record):
        record.user = _current_user.get()
        return True
