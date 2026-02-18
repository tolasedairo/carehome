from django import forms
from .models import Resident


class ResidentForm(forms.ModelForm):
    """
    Form for creating and editing a resident.
    We manually style fields using Bootstrap classes.
    """

    class Meta:
        model = Resident
        fields = [
            "first_name",
            "last_name",
            "room_number",
            "gender",
            "date_of_birth",
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
