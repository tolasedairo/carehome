from django.urls import path
from .views import IncidentListView, IncidentCreateView, IncidentDetailView, IncidentUpdateView

app_name = 'incidents'

urlpatterns = [
    path('', IncidentListView.as_view(), name='list'),
    path('create/', IncidentCreateView.as_view(), name='create'),
    path('<int:pk>/', IncidentDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', IncidentUpdateView.as_view(), name='edit'),
]
