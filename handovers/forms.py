from django import forms
from .models import Handover


class HandoverForm(forms.ModelForm):
    class Meta:
        model = Handover
        fields = [
            'title',
            'resident',
            'shift',
            'priority',
            'notes',
            'is_completed'
        ]
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter handover title'}
            ),
            'resident': forms.Select(attrs={'class': 'form-select'}),
            'shift': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Write detailed handover notes...'
                }
            ),
            'is_completed': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }
