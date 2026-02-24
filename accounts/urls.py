from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path(
        'password/reset/done/',
        views.CustomPasswordResetDoneView.as_view(),
        name='account_reset_password_done'
    ),
    path('pending/', views.pending_approval, name='pending'),
    path('pending-users/', views.pending_users_list, name='pending-users'),
    path(
        'pending-users/approve/<int:user_id>/',
        views.approve_user,
        name='approve-user'
    ),
    path(
        'pending-users/reject/<int:user_id>/',
        views.reject_user,
        name='reject-user'
    ),
]
