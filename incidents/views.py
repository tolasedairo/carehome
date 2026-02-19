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
    paginate_by = 10

    def get_queryset(self):
        queryset = Incident.objects.all()
        resident_id = self.request.GET.get('resident')
        if resident_id:
            queryset = queryset.filter(resident_id=resident_id)
        return queryset

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
