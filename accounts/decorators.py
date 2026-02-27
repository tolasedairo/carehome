from functools import wraps
from django.shortcuts import redirect


def approval_required(view_func):
    """
    Decorator to check if user is approved before accessing protected views.
    Redirects unapproved users to pending approval page.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Check if user is approved
            if not request.user.is_approved:
                return redirect('accounts:pending')
        # If authenticated and approved, or if not required, continue
        return view_func(request, *args, **kwargs)

    return wrapper
