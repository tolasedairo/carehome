from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Field
from .models import Resident


class ResidentForm(forms.ModelForm):
    """
    Form for creating and editing a resident.
    We manually style fields using Bootstrap classes.
    """

    class Meta:
        model = Resident
        fields = [
            'first_name',
            'last_name',
            'date_of_birth',
            'gender',
            'room_number',
            'emergency_contact_name',
            'emergency_contact_phone',
            'medical_notes',
            'profile_picture'
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap styling to every field
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control"
            })

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Personal Information",
                Row(
                    Column("first_name", css_class="col-md-6"),
                    Column("last_name", css_class="col-md-6"),
                ),
                Row(
                    Column("date_of_birth", css_class="col-md-6"),
                    Column("gender", css_class="col-md-6"),
                ),
                Row(
                    Column("room_number", css_class="col-md-6"),
                    Column("profile_picture", css_class="col-md-6"),
                ),
            ),
            Fieldset(
                "Emergency Contact",
                Row(
                    Column("emergency_contact_name", css_class="col-md-6"),
                    Column("emergency_contact_phone", css_class="col-md-6"),
                ),
            ),
            Fieldset(
                "Medical Information",
                Field("medical_notes"),
            ),
        )
