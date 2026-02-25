from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column("resident", css_class="col-md-6"),
                Column("incident_type", css_class="col-md-6"),
            ),
            Field("description"),
            Field("is_resolved"),
        )
