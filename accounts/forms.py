from allauth.account.forms import LoginForm, SignupForm
from django import forms
from .models import CustomUser


class CustomLoginForm(LoginForm):
    """
    Custom login form for allauth.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].label = 'Email or Username'
        self.fields['login'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your email or username',
            'autocomplete': 'username',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password',
        })
        # Remove help text to prevent aria-describedby
        self.fields['password'].help_text = ''


class CustomSignupForm(SignupForm):
    """
    Custom signup form for allauth with role selection.
    """
    first_name = forms.CharField(
        max_length=150,
        label='First Name',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your first name',
        })
    )

    last_name = forms.CharField(
        max_length=150,
        label='Last Name',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your last name',
        })
    )

    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        label='Your Role',
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update email field
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'you@example.com',
        })
        # Update password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a strong password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password',
        })
        # Remove help text to prevent aria-describedby
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        # Remove username field label customization if needed
        if 'username' in self.fields:
            self.fields['username'].widget.attrs.update({
                'class': 'form-control',
            })

    def save(self, request):
        user = super().save(request)
        # Set the additional fields
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = self.cleaned_data['role']
        user.is_approved = False  # New users require approval
        user.save()
        return user
