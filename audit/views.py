from django.views.generic import ListView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from accounts.decorators import approval_required
from .models import AuditLog

# Create your views here.


@method_decorator([login_required, approval_required], name='dispatch')
class AuditLogListView(ListView):
    model = AuditLog
    template_name = 'audit/audit_log_list.html'
    context_object_name = 'logs'
    paginate_by = 20

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != "MANAGER" and not (
            request.user.is_staff or request.user.is_superuser
        ):
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = AuditLog.objects.select_related('user')

        # Search by user or description
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(user__username__icontains=search_query) |
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        # Filter by action
        action = self.request.GET.get('action', '')
        if action:
            queryset = queryset.filter(action=action)

        # Filter by date range
        date_from = self.request.GET.get('date_from', '')
        date_to = self.request.GET.get('date_to', '')
        if date_from:
            queryset = queryset.filter(timestamp__gte=date_from)
        if date_to:
            queryset = queryset.filter(timestamp__lte=date_to)

        return queryset.order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_choices'] = AuditLog.ACTION_CHOICES
        context['total_logs'] = AuditLog.objects.count()
        return context
