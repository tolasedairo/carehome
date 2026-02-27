from django.urls import path
from .views import (
    CarePlanListView,
    ArchivedCarePlanListView,
    CarePlanCreateView,
    CarePlanDetailView,
    CarePlanUpdateView,
    archive_careplan,
    unarchive_careplan,
)

app_name = 'careplans'

urlpatterns = [
    path('', CarePlanListView.as_view(), name='list'),
    path('archived/', ArchivedCarePlanListView.as_view(), name='archived'),
    path('create/', CarePlanCreateView.as_view(), name='create'),
    path('<int:pk>/', CarePlanDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', CarePlanUpdateView.as_view(), name='edit'),
    path('<int:pk>/archive/', archive_careplan, name='archive'),
    path('<int:pk>/unarchive/', unarchive_careplan, name='unarchive'),
]
