from django.urls import path
from . import views

app_name = 'residents'

urlpatterns = [
    path('', views.ResidentListView.as_view(), name='list'),
    path('archived/', views.ArchivedResidentListView.as_view(), name='archived'),
    path('create/', views.ResidentCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ResidentDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ResidentUpdateView.as_view(), name='edit'),
    path('<int:pk>/archive/', views.archive_resident, name='archive'),
    path('<int:pk>/unarchive/', views.unarchive_resident, name='unarchive'),
]
