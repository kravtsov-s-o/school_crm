import contextvars
import logging

_current_user = contextvars.ContextVar("current_user", default="anonymous")


def set_current_user(user):
    _current_user.set(user)


class CurrentUserFilter(logging.Filter):
    def filter(self, record):
        record.user = _current_user.get()
        return True
