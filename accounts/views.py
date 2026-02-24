from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from allauth.account.views import PasswordResetDoneView
from .models import CustomUser
from audit.models import AuditLog


@login_required
def pending_approval(request):
    """
    View displayed to users awaiting admin approval.
    """
    return render(request, 'accounts/pending_approval.html')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


@login_required
def pending_users_list(request):
    """
    View for managers to see and approve pending users.
    """
    if request.user.role != "MANAGER":
        messages.error(request, "You don't have permission to view this page.")
        return redirect('dashboard:home')

    # Get all unapproved users
    pending_users = CustomUser.objects.filter(is_approved=False).order_by(
        '-date_joined'
    )

    context = {
        'pending_users': pending_users,
    }

    return render(request, 'accounts/pending_users_list.html', context)


@login_required
def approve_user(request, user_id):
    """
    View for managers to approve a pending user.
    """
    if request.user.role != "MANAGER":
        messages.error(
            request,
            "You don't have permission to perform this action."
        )
        return redirect('dashboard:home')

    user = get_object_or_404(CustomUser, id=user_id)

    if not user.is_approved:
        user.is_approved = True
        user.save()
        AuditLog.objects.create(
            user=request.user,
            action='USER_APPROVAL',
            target_model='CustomUser',
            target_id=user.id,
            description=(
                f"Approved user: {user.get_full_name() or user.username}"
            )
        )
        messages.success(
            request,
            f"User {user.get_full_name() or user.username} "
            "has been approved!"
        )
    else:
        messages.info(request, "This user is already approved.")

    return redirect('accounts:pending-users')


@login_required
def reject_user(request, user_id):
    """
    View for managers to reject/deactivate a pending user.
    """
    if request.user.role != "MANAGER":
        messages.error(
            request,
            "You don't have permission to perform this action."
        )
        return redirect('dashboard:home')

    user = get_object_or_404(CustomUser, id=user_id)

    if not user.is_approved:
        user.is_active = False
        user.save()
        messages.success(
            request,
            f"User {user.get_full_name() or user.username} "
            "has been rejected."
        )
    else:
        messages.error(request, "Cannot reject an already approved user.")

    return redirect('accounts:pending-users')
