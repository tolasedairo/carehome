from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import Resident
from .forms import ResidentForm
from accounts.decorators import approval_required

# Create your views here.
# This code defines views for managing residents in the care home application.


@method_decorator([login_required, approval_required], name='dispatch')
class ResidentListView(ListView):
    """Display all active residents"""
    model = Resident
    template_name = 'residents/resident_list.html'
    context_object_name = 'residents'
    paginate_by = 20

    def get_queryset(self):
        # Start with all residents, filter by status later
        status = self.request.GET.get('status', '')

        if status == 'archived':
            queryset = Resident.objects.filter(is_active=False)
        else:
            queryset = Resident.objects.filter(is_active=True)

        # Search by name
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )

        # Annotate with incident counts
        queryset = queryset.annotate(
            incident_count=Count('incidents'),
            open_incident_count=Count('incidents', filter=Q(incidents__is_resolved=False))
        )

        return queryset


# Manager-only views for archived residents and resident management
@method_decorator([login_required, approval_required], name='dispatch')
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


@method_decorator([login_required, approval_required], name='dispatch')
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


# Detail and Update views are accessible to all logged-in users,
# but only managers can edit or archive residents.
@method_decorator([login_required, approval_required], name='dispatch')
class ResidentDetailView(DetailView):
    """Display detailed information about a resident"""
    model = Resident
    template_name = 'residents/resident_detail.html'
    context_object_name = 'resident'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get incidents related to this resident
        context['incidents'] = self.object.incidents.select_related(
            'created_by'
        ).order_by('-created_at')[:10]
        context['incident_count'] = self.object.incidents.count()
        context['open_incident_count'] = self.object.incidents.filter(
            is_resolved=False
        ).count()
        return context


# Only managers can edit or archive residents, but anyone can view details
@method_decorator([login_required, approval_required], name='dispatch')
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


# These functions handle archiving and unarchiving residents,
# which is only allowed for managers.
@login_required
@approval_required
def archive_resident(request, pk):
    """Archive a resident (mark as inactive)"""
    if request.user.role != "MANAGER":
        return redirect('residents:list')

    resident = get_object_or_404(Resident, pk=pk)
    resident.is_active = False
    resident.save()
    return redirect('residents:detail', pk=pk)


# This function allows managers to restore an archived resident
# by marking them as active again.
@login_required
@approval_required
def unarchive_resident(request, pk):
    """Restore an archived resident (mark as active)"""
    if request.user.role != "MANAGER":
        return redirect('residents:list')

    resident = get_object_or_404(Resident, pk=pk)
    resident.is_active = True
    resident.save()
    return redirect('residents:detail', pk=pk)


def resident_list(request):
    residents = Resident.objects.filter(
        is_active=True
    ).order_by('last_name')

    paginator = Paginator(residents, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'residents': page_obj}
    return render(request, 'residents/resident_list.html', context)

