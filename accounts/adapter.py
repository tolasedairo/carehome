from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_signup_redirect_url(self, request):
        return reverse('accounts:pending')

    def get_login_redirect_url(self, request):
        if request.user.is_authenticated and not request.user.is_approved:
            return reverse('accounts:pending')
        return super().get_login_redirect_url(request)
