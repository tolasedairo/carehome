from django import forms
from .models import Incident


class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = [
            'resident',
            'incident_type',
            'description',
            'is_resolved'
        ]
        widgets = {
            'description': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control'}
            ),
            'resident': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'incident_type': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'is_resolved': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }
