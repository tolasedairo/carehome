from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.decorators import approval_required
from .models import Incident
from .forms import IncidentForm

# Create your views here.
@method_decorator([login_required, approval_required], name='dispatch')
class IncidentListView(ListView):
    model = Incident
    template_name = 'incidents/incident_list.html'
    context_object_name = 'incidents'
    paginate_by = 20

    def get_queryset(self):
        queryset = Incident.objects.select_related('resident', 'created_by')
        
        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(description__icontains=search_query) |
                Q(resident__first_name__icontains=search_query) |
                Q(resident__last_name__icontains=search_query)
            )
        
        # Filter by incident type
        incident_type = self.request.GET.get('incident_type', '')
        if incident_type:
            queryset = queryset.filter(incident_type=incident_type)
        
        # Filter by status
        status = self.request.GET.get('status', '')
        if status == 'resolved':
            queryset = queryset.filter(is_resolved=True)
        elif status == 'open':
            queryset = queryset.filter(is_resolved=False)
        
        # Filter by resident
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
        return context

@method_decorator([login_required, approval_required], name='dispatch')
class IncidentCreateView(CreateView):
    model = Incident
    form_class = IncidentForm
    template_name = 'incidents/incident_form.html'
    success_url = reverse_lazy('incidents:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

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
