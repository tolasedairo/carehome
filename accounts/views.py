from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def pending_approval(request):
    """
    View displayed to users awaiting admin approval.
    """
    return render(request, 'accounts/pending_approval.html')
