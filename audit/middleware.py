import threading

_thread_locals = threading.local()


def get_current_user():
    """
    Retrieve the current user from thread-local storage.
    Returns None if no user is set.
    """
    return getattr(_thread_locals, 'user', None)


def set_current_user(user):
    """
    Store the current user in thread-local storage.
    """
    _thread_locals.user = user


class CurrentUserMiddleware:
    """
    Middleware to store the current user in thread-local storage
    so it can be accessed in signals and other places without request context.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            set_current_user(request.user)
        else:
            set_current_user(None)

        response = self.get_response(request)

        # Clean up after request
        set_current_user(None)

        return response
