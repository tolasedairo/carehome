from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column("title", css_class="col-md-6"),
                Column("resident", css_class="col-md-6"),
            ),
            Row(
                Column("shift", css_class="col-md-4"),
                Column("priority", css_class="col-md-4"),
                Column("is_completed", css_class="col-md-4"),
            ),
            Field("notes"),
        )
