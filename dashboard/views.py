from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    """
    Basic dashboard placeholder.
    """
    if not request.user.is_approved:
        messages.warning(request, "Your account is pending approval.")
    return render(request, 'dashboard/home.html')