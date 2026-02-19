from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView
)
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.contrib import messages
from accounts.decorators import approval_required
from .models import Handover
from .forms import HandoverForm

# Create your views here.


@method_decorator([login_required, approval_required], name='dispatch')
class HandoverListView(ListView):
    model = Handover
    template_name = 'handovers/handover_list.html'
    context_object_name = 'handovers'
    paginate_by = 20

    def get_queryset(self):
        queryset = Handover.objects.select_related(
            'resident', 'created_by'
        )
        
        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(notes__icontains=search_query) |
                Q(resident__first_name__icontains=search_query) |
                Q(resident__last_name__icontains=search_query)
            )
        
        # Filter by shift
        shift = self.request.GET.get('shift', '')
        if shift:
            queryset = queryset.filter(shift=shift)
        
        # Filter by priority
        priority = self.request.GET.get('priority', '')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        # Filter by completion status
        status = self.request.GET.get('status', '')
        if status == 'completed':
            queryset = queryset.filter(is_completed=True)
        elif status == 'pending':
            queryset = queryset.filter(is_completed=False)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_shift'] = self.request.GET.get('shift', '')
        context['selected_priority'] = self.request.GET.get('priority', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['shift_choices'] = Handover.SHIFT_CHOICES
        context['priority_choices'] = Handover.PRIORITY_CHOICES
        
        # Add quick stats
        all_handovers = Handover.objects.all()
        context['total_handovers'] = all_handovers.count()
        context['pending_handovers'] = all_handovers.filter(
            is_completed=False
        ).count()
        context['completed_handovers'] = all_handovers.filter(
            is_completed=True
        ).count()
        
        return context


@method_decorator([login_required, approval_required], name='dispatch')
class HandoverCreateView(CreateView):
    model = Handover
    form_class = HandoverForm
    template_name = 'handovers/handover_form.html'
    success_url = reverse_lazy('handovers:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(
            self.request,
            'Handover has been created successfully.'
        )
        return super().form_valid(form)


@method_decorator([login_required, approval_required], name='dispatch')
class HandoverDetailView(DetailView):
    model = Handover
    template_name = 'handovers/handover_detail.html'
    context_object_name = 'handover'


@method_decorator([login_required, approval_required], name='dispatch')
class HandoverUpdateView(UpdateView):
    model = Handover
    form_class = HandoverForm
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

        return HttpResponseForbidden(
            "You do not have permission to edit this handover."
        )

    def form_valid(self, form):
        messages.success(
            self.request,
            'Handover has been updated successfully.'
        )
        return super().form_valid(form)