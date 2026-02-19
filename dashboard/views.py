from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from residents.models import Resident
from incidents.models import Incident
from accounts.models import CustomUser
from accounts.decorators import approval_required


@login_required
@approval_required
def home(request):
    """
    Dashboard with resident and incident statistics.
    """
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

    # Calculate incident statistics
    total_incidents = Incident.objects.count()
    open_incidents = Incident.objects.filter(is_resolved=False).count()
    resolved_incidents = Incident.objects.filter(is_resolved=True).count()
    recent_incidents_count = Incident.objects.filter(
        created_at__gte=last_week
    ).count()

    # Get list of 5 most recent incidents
    recent_incidents_list = Incident.objects.select_related(
        'resident', 'created_by'
    ).order_by('-created_at')[:5]

    # Manager-only: Get pending user approvals
    pending_users_count = 0
    pending_users_list = []

    if request.user.role == "MANAGER":
        pending_users_count = CustomUser.objects.filter(
            is_approved=False
        ).count()
        pending_users_list = CustomUser.objects.filter(
            is_approved=False
        ).order_by('-date_joined')[:5]

    context = {
        'total_residents': total_residents,
        'active_residents': active_residents,
        'archived_residents': archived_residents,
        'recent_residents': recent_residents,
        'recent_list': recent_list,
        'total_incidents': total_incidents,
        'open_incidents': open_incidents,
        'resolved_incidents': resolved_incidents,
        'recent_incidents_count': recent_incidents_count,
        'recent_incidents_list': recent_incidents_list,
        'pending_users_count': pending_users_count,
        'pending_users_list': pending_users_list,
    }

    return render(request, 'dashboard/home.html', context)
