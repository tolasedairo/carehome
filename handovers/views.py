from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView
)
from django.urls import reverse_lazy
from .models import Handover

# Create your views here.


class HandoverListView(LoginRequiredMixin, ListView):
    model = Handover
    template_name = 'handovers/handover_list.html'
    context_object_name = 'handovers'
    paginate_by = 20


class HandoverCreateView(LoginRequiredMixin, CreateView):
    model = Handover
    fields = ['title', 'resident', 'shift', 'notes']
    template_name = 'handovers/handover_form.html'
    success_url = reverse_lazy('handovers:list')


class HandoverDetailView(LoginRequiredMixin, DetailView):
    model = Handover
    template_name = 'handovers/handover_detail.html'
    context_object_name = 'handover'


class HandoverUpdateView(LoginRequiredMixin, UpdateView):
    model = Handover
    fields = ['title', 'resident', 'shift', 'notes']
    template_name = 'handovers/handover_form.html'
    success_url = reverse_lazy('handovers:list')

    def dispatch(self, request, *args, **kwargs):
        handover = self.get_object()

        # Allow manager
        if request.user.role == "MANAGER":
            return super().dispatch(request, *args, **kwargs)

        # Allow original author
        if handover.created_by == request.user:
            return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden("You do not have permission to edit this handover.")