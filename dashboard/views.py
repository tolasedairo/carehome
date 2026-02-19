from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from residents.models import Resident


@login_required
def home(request):
    """
    Dashboard with resident statistics.
    """
    if not request.user.is_approved:
        messages.warning(request, "Your account is pending approval.")
    
    # Calculate resident statistics
    total_residents = Resident.objects.count()
    active_residents = Resident.objects.filter(is_active=True).count()
    archived_residents = Resident.objects.filter(is_active=False).count()

    last_week = timezone.now() - timedelta(days=7)
    recent_residents = Resident.objects.filter(
        created_at__gte=last_week
    ).count()

    # Get list of 5 most recent residents
    recent_list = Resident.objects.order_by('-created_at')[:5]

    context = {
        'total_residents': total_residents,
        'active_residents': active_residents,
        'archived_residents': archived_residents,
        'recent_residents': recent_residents,
        'recent_list': recent_list,
    }

    return render(request, 'dashboard/home.html', context)
