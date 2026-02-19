from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from .models import Resident
from .forms import ResidentForm


@method_decorator(login_required, name='dispatch')
class ResidentListView(ListView):
    """Display all active residents"""
    model = Resident
    template_name = 'residents/resident_list.html'
    context_object_name = 'residents'
    paginate_by = 20

    def get_queryset(self):
        return Resident.objects.filter(is_active=True)


@method_decorator(login_required, name='dispatch')
class ResidentCreateView(CreateView):
    """Allow managers to create new residents"""
    model = Resident
    form_class = ResidentForm
    template_name = 'residents/resident_form.html'
    success_url = reverse_lazy('residents:list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != "MANAGER":
            return redirect('residents:list')
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ResidentDetailView(DetailView):
    """Display detailed information about a resident"""
    model = Resident
    template_name = 'residents/resident_detail.html'
    context_object_name = 'resident'

