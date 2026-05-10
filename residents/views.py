from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import Resident
from careplans.models import CarePlan
from careplans.forms import CarePlanForm
from .forms import ResidentForm
from accounts.decorators import approval_required


@login_required
@approval_required
def delete_resident_select(request):
    """Placeholder view for manager-only delete selection page.

    Currently not implemented (safe placeholder). Managers see a message
    and are redirected back to the residents list. This enforces role
    protection server-side in Stage 2 without enabling destructive actions.
    """
    if request.user.role != "MANAGER":
        messages.error(request, 'Only managers can access resident deletion.')
        return redirect('residents:list')

    # Show archived residents to choose for permanent deletion.
    archived = Resident.objects.filter(is_active=False).order_by('last_name', 'first_name')
    context = {'residents': archived}
    return render(request, 'residents/resident_delete_select.html', context)


@login_required
@approval_required
def delete_resident(request, pk):
    """Placeholder delete endpoint that enforces manager-only access.

    This intentionally does not perform deletion in Stage 2. If accessed,
    it will refuse and redirect to the list to keep data safe.
    """
    if request.user.role != "MANAGER":
        messages.error(request, 'Only managers can delete residents.')
        return redirect('residents:list')

    # Only allow POST for destructive actions; block for now.
    if request.method != 'POST':
        messages.error(request, 'Resident deletion requires a POST request. Feature not enabled yet.')
        return redirect('residents:list')

    messages.error(request, 'Resident deletion is not enabled yet. Complete the next implementation stage to enable.')
    return redirect('residents:list')


@method_decorator([login_required, approval_required], name='dispatch')
class ResidentListView(ListView):
    """Display all active residents"""
    model = Resident
    template_name = 'residents/resident_list.html'
    context_object_name = 'residents'
    paginate_by = 20

    def get_queryset(self):
        status = self.request.GET.get('status', '')
        if status == 'archived':
            queryset = Resident.objects.filter(is_active=False)
        else:
            queryset = Resident.objects.filter(is_active=True)

        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )

        queryset = queryset.annotate(
            incident_count=Count('incidents', distinct=True),
            open_incident_count=Count(
                'incidents',
                filter=Q(incidents__is_resolved=False),
                distinct=True
            )
        ).order_by(
            'last_name', 'first_name'
        ).distinct()  # Pagination fix

        return queryset


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
        return Resident.objects.filter(
            is_active=False
        ).order_by('last_name', 'first_name')


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        careplan_form = CarePlanForm(self.request.POST or None)
        careplan_form.fields['resident'].required = False
        careplan_form.fields['review_date'].required = True
        context['careplan_form'] = careplan_form
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        careplan_form = CarePlanForm(request.POST)
        careplan_form.fields['resident'].required = False
        careplan_form.fields['review_date'].required = True

        if form.is_valid() and careplan_form.is_valid():
            return self.forms_valid(form, careplan_form)
        return self.forms_invalid(form, careplan_form)

    def forms_valid(self, form, careplan_form):
        resident = form.save(commit=False)
        resident.created_by = self.request.user
        resident.save()
        self.object = resident

        if self._has_careplan_data(careplan_form):
            careplan = careplan_form.save(commit=False)
            careplan.resident = resident
            careplan.created_by = self.request.user
            careplan.is_active = True
            careplan.save()
            messages.success(
                self.request,
                f'Resident "{resident.first_name} '
                f'{resident.last_name}" and care plan created '
                f'successfully.'
            )
        else:
            messages.success(
                self.request,
                f'Resident "{resident.first_name} '
                f'{resident.last_name}" created successfully.'
            )

        return redirect(self.get_success_url())

    def forms_invalid(self, form, careplan_form):
        return self.render_to_response(
            self.get_context_data(form=form, careplan_form=careplan_form)
        )

    def _has_careplan_data(self, careplan_form):
        for value in careplan_form.cleaned_data.values():
            if value not in (None, "", [], ()):
                return True
        return False


@method_decorator([login_required, approval_required], name='dispatch')
class ResidentDetailView(DetailView):
    """Display detailed information about a resident"""
    model = Resident
    template_name = 'residents/resident_detail.html'
    context_object_name = 'resident'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['incidents'] = self.object.incidents.select_related(
            'created_by'
        ).order_by('-created_at')[:10]
        context['incident_count'] = self.object.incidents.count()
        context['open_incident_count'] = (
            self.object.incidents.filter(is_resolved=False).count()
        )
        context['careplans'] = self.object.care_plans.filter(
            is_active=True
        ).order_by('-updated_at')
        return context


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

    def get_careplan_instance(self):
        return CarePlan.objects.filter(
            resident=self.object, is_active=True
        ).order_by('-updated_at').first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        careplan_instance = self.get_careplan_instance()
        careplan_form = CarePlanForm(
            self.request.POST or None, instance=careplan_instance
        )
        careplan_form.fields['resident'].required = False
        context['careplan_form'] = careplan_form
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        careplan_instance = self.get_careplan_instance()
        careplan_form = CarePlanForm(
            request.POST, instance=careplan_instance
        )
        careplan_form.fields['resident'].required = False

        if form.is_valid() and careplan_form.is_valid():
            return self.forms_valid(form, careplan_form)
        return self.forms_invalid(form, careplan_form)

    def forms_valid(self, form, careplan_form):
        resident = form.save()
        if self._has_careplan_data(careplan_form):
            careplan = careplan_form.save(commit=False)
            careplan.resident = resident
            if not careplan.created_by:
                careplan.created_by = self.request.user
            careplan.is_active = True
            careplan.save()
            messages.success(
                self.request,
                f'Resident "{resident.first_name} '
                f'{resident.last_name}" and care plan updated '
                f'successfully.'
            )
        else:
            messages.success(
                self.request,
                f'Resident "{resident.first_name} '
                f'{resident.last_name}" updated successfully.'
            )
        return redirect(self.get_success_url())

    def forms_invalid(self, form, careplan_form):
        return self.render_to_response(
            self.get_context_data(form=form, careplan_form=careplan_form)
        )

    def _has_careplan_data(self, careplan_form):
        for value in careplan_form.cleaned_data.values():
            if value not in (None, "", [], ()):
                return True
        return False


@login_required
@approval_required
def archive_resident(request, pk):
    """Archive a resident (mark as inactive)"""
    if request.user.role != "MANAGER":
        messages.error(
            request, 'Only managers can archive residents.'
        )
        return redirect('residents:list')
    resident = get_object_or_404(Resident, pk=pk)
    resident.is_active = False
    resident.save()
    messages.success(
        request,
        f'Resident "{resident.first_name} {resident.last_name}" '
        f'has been archived.'
    )
    return redirect('residents:detail', pk=pk)


@login_required
@approval_required
def unarchive_resident(request, pk):
    """Restore an archived resident (mark as active)"""
    if request.user.role != "MANAGER":
        messages.error(
            request,
            'Only managers can restore archived residents.'
        )
        return redirect('residents:list')
    resident = get_object_or_404(Resident, pk=pk)
    resident.is_active = True
    resident.save()
    messages.success(
        request,
        f'Resident "{resident.first_name} {resident.last_name}" '
        f'has been restored.'
    )
    return redirect('residents:detail', pk=pk)


def resident_list(request):
    """Function-based view for resident list with pagination"""
    # Pagination fix due to distinct() removing ordering
    residents = Resident.objects.filter(is_active=True).order_by(
        'last_name', 'first_name'
    )
    paginator = Paginator(residents, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'residents': page_obj}
    return render(request, 'residents/resident_list.html', context)
