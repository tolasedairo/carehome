from django import forms
from .models import CarePlan


class CarePlanForm(forms.ModelForm):
    class Meta:
        model = CarePlan
        fields = [
            "resident",
            "title",
            "review_date",
            "assessment_summary",
            "personal_care",
            "mobility",
            "nutrition",
            "medication",
            "communication",
            "wellbeing",
            "skin_integrity",
            "daily_routine",
            "safeguarding_risks",
        ]
        widgets = {
            "review_date": forms.DateInput(attrs={"type": "date"}),
            "assessment_summary": forms.Textarea(attrs={"rows": 4}),
            "personal_care": forms.Textarea(attrs={"rows": 4}),
            "mobility": forms.Textarea(attrs={"rows": 4}),
            "nutrition": forms.Textarea(attrs={"rows": 4}),
            "medication": forms.Textarea(attrs={"rows": 4}),
            "communication": forms.Textarea(attrs={"rows": 4}),
            "wellbeing": forms.Textarea(attrs={"rows": 4}),
            "skin_integrity": forms.Textarea(attrs={"rows": 4}),
            "daily_routine": forms.Textarea(attrs={"rows": 4}),
            "safeguarding_risks": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name == "resident":
                field.widget.attrs.update({"class": "form-select"})
            else:
                field.widget.attrs.update({"class": "form-control"})
