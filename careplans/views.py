from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect

from .models import CarePlan


# Create your views here.


class CarePlanListView(LoginRequiredMixin, ListView):
    model = CarePlan
    template_name = 'careplans/careplan_list.html'
    context_object_name = 'careplans'

    def get_queryset(self):
        return CarePlan.objects.filter(is_active=True)


class ArchivedCarePlanListView(LoginRequiredMixin, ListView):
    model = CarePlan
    template_name = 'careplans/careplan_list.html'
    context_object_name = 'careplans'

    def get_queryset(self):
        return CarePlan.objects.filter(is_active=False)


class CarePlanCreateView(LoginRequiredMixin, CreateView):
    model = CarePlan
    fields = ['resident', 'title', 'description', 'review_date']
    template_name = 'careplans/careplan_form.html'
    success_url = reverse_lazy('careplans:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class CarePlanDetailView(LoginRequiredMixin, DetailView):
    model = CarePlan
    template_name = 'careplans/careplan_detail.html'


class CarePlanUpdateView(LoginRequiredMixin, UpdateView):
    model = CarePlan
    fields = ['resident', 'title', 'description', 'review_date']
    template_name = 'careplans/careplan_form.html'
    success_url = reverse_lazy('careplans:list')

    def dispatch(self, request, *args, **kwargs):
        careplan = self.get_object()

        if request.user.role == "MANAGER":
            return super().dispatch(request, *args, **kwargs)

        if careplan.created_by == request.user:
            return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden("You do not have permission to edit this care plan.")
    
    
def archive_careplan(request, pk):
    careplan = get_object_or_404(CarePlan, pk=pk)

    if request.user.role != "MANAGER":
        return HttpResponseForbidden("Only managers can archive care plans.")

    careplan.is_active = False
    careplan.save()
    return redirect('careplans:list')


def unarchive_careplan(request, pk):
    careplan = get_object_or_404(CarePlan, pk=pk)

    if request.user.role != "MANAGER":
        return HttpResponseForbidden("Only managers can unarchive care plans.")

    careplan.is_active = True
    careplan.save()
    return redirect('careplans:archived')