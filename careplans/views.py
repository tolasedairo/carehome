from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from accounts.decorators import approval_required
from .models import CarePlan
from .forms import CarePlanForm



# Create your views here.
@method_decorator([login_required, approval_required], name='dispatch')
class CarePlanListView(ListView):
    model = CarePlan
    template_name = 'careplans/careplan_list.html'
    context_object_name = 'careplans'

    def get_queryset(self):
        return CarePlan.objects.filter(is_active=True).select_related(
            'resident', 'created_by'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()
        context['is_archived'] = False
        return context


@method_decorator([login_required, approval_required], name='dispatch')
class ArchivedCarePlanListView(ListView):
    model = CarePlan
    template_name = 'careplans/careplan_list.html'
    context_object_name = 'careplans'

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != "MANAGER":
            return redirect('careplans:list')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return CarePlan.objects.filter(is_active=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()
        context['is_archived'] = True
        return context


@method_decorator([login_required, approval_required], name='dispatch')
class CarePlanCreateView(CreateView):
    model = CarePlan
    form_class = CarePlanForm
    template_name = 'careplans/careplan_form.html'
    success_url = reverse_lazy('careplans:list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != "MANAGER":
            return redirect('careplans:list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


@method_decorator([login_required, approval_required], name='dispatch')
class CarePlanDetailView(DetailView):
    model = CarePlan
    template_name = 'careplans/careplan_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()
        return context


@method_decorator([login_required, approval_required], name='dispatch')
class CarePlanUpdateView(UpdateView):
    model = CarePlan
    form_class = CarePlanForm
    template_name = 'careplans/careplan_form.html'
    success_url = reverse_lazy('careplans:list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.role == "SENIOR":
            form.fields['resident'].disabled = True
        return form

    def dispatch(self, request, *args, **kwargs):
        if request.user.role in ["MANAGER", "SENIOR"]:
            return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden("You do not have permission to edit this care plan.")
    
    
@login_required
@approval_required
def archive_careplan(request, pk):
    careplan = get_object_or_404(CarePlan, pk=pk)

    if request.user.role != "MANAGER":
        return HttpResponseForbidden("Only managers can archive care plans.")

    careplan.is_active = False
    careplan.save()
    return redirect('careplans:list')


@login_required
@approval_required
def unarchive_careplan(request, pk):
    careplan = get_object_or_404(CarePlan, pk=pk)

    if request.user.role != "MANAGER":
        return HttpResponseForbidden("Only managers can unarchive care plans.")

    careplan.is_active = True
    careplan.save()
    return redirect('careplans:archived')