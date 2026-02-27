from django.views.generic import ListView, CreateView, DetailView, UpdateView, View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q

from accounts.decorators import approval_required
from .models import Incident
from .forms import IncidentForm
from audit.models import AuditLog


@method_decorator([login_required, approval_required], name='dispatch')
class IncidentListView(ListView):
    model = Incident
    template_name = 'incidents/incident_list.html'
    context_object_name = 'incidents'
    paginate_by = 20

    def get_queryset(self):
        queryset = Incident.objects.select_related('resident', 'created_by').order_by('-created_at')

        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(description__icontains=search_query) |
                Q(resident__first_name__icontains=search_query) |
                Q(resident__last_name__icontains=search_query)
            )

        incident_type = self.request.GET.get('incident_type', '')
        if incident_type:
            queryset = queryset.filter(incident_type=incident_type)

        status = self.request.GET.get('status', '')
        if status == 'resolved':
            queryset = queryset.filter(is_resolved=True)
        elif status == 'open':
            queryset = queryset.filter(is_resolved=False)

        resident_id = self.request.GET.get('resident')
        if resident_id:
            queryset = queryset.filter(resident_id=resident_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_type'] = self.request.GET.get('incident_type', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['incident_types'] = Incident.INCIDENT_TYPE_CHOICES

        all_incidents = Incident.objects.all()
        context['total_incidents'] = all_incidents.count()
        context['open_incidents'] = all_incidents.filter(is_resolved=False).count()
        context['resolved_incidents'] = all_incidents.filter(is_resolved=True).count()

        return context


@method_decorator([login_required, approval_required], name='dispatch')
class IncidentCreateView(CreateView):
    model = Incident
    form_class = IncidentForm
    template_name = 'incidents/incident_form.html'
    success_url = reverse_lazy('incidents:list')

    def get_initial(self):
        initial = super().get_initial()
        resident_id = self.request.GET.get('resident')
        if resident_id:
            initial['resident'] = resident_id
        return initial

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)

        # ✅ Audit Log
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE_INCIDENT',
            target_model='Incident',
            target_id=self.object.id,
            description=f'Incident created for resident {self.object.resident}'
        )

        messages.success(
            self.request,
            'Incident report has been created successfully.'
        )
        return response


@method_decorator([login_required, approval_required], name='dispatch')
class IncidentDetailView(DetailView):
    model = Incident
    template_name = 'incidents/incident_detail.html'


@method_decorator([login_required, approval_required], name='dispatch')
class IncidentUpdateView(UpdateView):
    model = Incident
    form_class = IncidentForm
    template_name = 'incidents/incident_form.html'
    success_url = reverse_lazy('incidents:list')

    def form_valid(self, form):
        response = super().form_valid(form)

        # ✅ Audit Log
        AuditLog.objects.create(
            user=self.request.user,
            action='UPDATE_INCIDENT',
            target_model='Incident',
            target_id=self.object.id,
            description='Incident updated'
        )

        messages.success(
            self.request,
            'Incident report has been updated successfully.'
        )
        return response


@method_decorator([login_required, approval_required], name='dispatch')
class IncidentResolveView(View):
    """Mark incident as resolved (Manager only)"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'MANAGER':
            messages.error(request, 'Only managers can resolve incidents.')
            return redirect('incidents:list')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, pk):
        incident = get_object_or_404(Incident, pk=pk)
        incident.is_resolved = True
        incident.save()

        # ✅ Audit Log
        AuditLog.objects.create(
            user=request.user,
            action='RESOLVE_INCIDENT',
            target_model='Incident',
            target_id=incident.id,
            description=f'Incident resolved for resident {incident.resident}'
        )

        messages.success(request, 'Incident has been marked as resolved.')
        return redirect('incidents:detail', pk=pk)


@method_decorator([login_required, approval_required], name='dispatch')
class IncidentUnresolveView(View):
    """Reopen a resolved incident (Manager only)"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'MANAGER':
            messages.error(request, 'Only managers can reopen incidents.')
            return redirect('incidents:list')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, pk):
        incident = get_object_or_404(Incident, pk=pk)
        incident.is_resolved = False
        incident.save()

        messages.success(request, 'Incident has been reopened.')
        return redirect('incidents:detail', pk=pk)
