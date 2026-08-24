from core.logging import set_current_user


class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            set_current_user(str(user))
        else:
            set_current_user("anonymous")
        return self.get_response(request)
