from django.urls import path
from .views import (
    HandoverListView,
    HandoverCreateView,
    HandoverDetailView,
    HandoverUpdateView,
)

app_name = 'handovers'

urlpatterns = [
    path('', HandoverListView.as_view(), name='list'),
    path('create/', HandoverCreateView.as_view(), name='create'),
    path('<int:pk>/', HandoverDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', HandoverUpdateView.as_view(), name='edit'),
]