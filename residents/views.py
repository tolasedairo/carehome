from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView
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
class ArchivedResidentListView(ListView):
    """Display all archived (inactive) residents - Manager only"""
    model = Resident
    template_name = 'residents/archived_resident_list.html'
    context_object_name = 'residents'
    paginate_by = 20

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != "MANAGER":
            return redirect('residents:list')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Resident.objects.filter(is_active=False)


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


@method_decorator(login_required, name='dispatch')
class ResidentUpdateView(UpdateView):
    """Allow managers to edit resident information"""
    model = Resident
    form_class = ResidentForm
    template_name = 'residents/resident_form.html'
    success_url = reverse_lazy('residents:list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != "MANAGER":
            return redirect('residents:list')
        return super().dispatch(request, *args, **kwargs)


@login_required
def archive_resident(request, pk):
    """Archive a resident (mark as inactive)"""
    if request.user.role != "MANAGER":
        return redirect('residents:list')
    
    resident = get_object_or_404(Resident, pk=pk)
    resident.is_active = False
    resident.save()
    return redirect('residents:detail', pk=pk)


@login_required
def unarchive_resident(request, pk):
    """Restore an archived resident (mark as active)"""
    if request.user.role != "MANAGER":
        return redirect('residents:list')
    
    resident = get_object_or_404(Resident, pk=pk)
    resident.is_active = True
    resident.save()
    return redirect('residents:detail', pk=pk)

