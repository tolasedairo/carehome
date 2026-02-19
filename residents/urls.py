from django.urls import path
from . import views

app_name = 'residents'

urlpatterns = [
    path('', views.ResidentListView.as_view(), name='list'),
    path('create/', views.ResidentCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ResidentDetailView.as_view(), name='detail'),  # Detail page
]
