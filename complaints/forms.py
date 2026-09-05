from django import forms

from .models import Complaint


class ComplaintForm(forms.ModelForm):

    class Meta:
        model = Complaint

        fields = [
            "complainant_name",
            "email",
            "phone",
            "category",
            "subject",
            "incident_date",
            "location",
            "description",
            "preferred_contact",
            "is_anonymous",
        ]

        widgets = {

            "complainant_name": forms.TextInput(
                attrs={
                    "placeholder": "Your name (optional)",
                    "autocomplete": "name",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "placeholder": "you@example.com",
                    "autocomplete": "email",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "placeholder": "+880 1XXXXXXXXX",
                    "autocomplete": "tel",
                }
            ),

            "subject": forms.TextInput(
                attrs={
                    "placeholder": "Brief subject of your complaint",
                }
            ),

            "incident_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "placeholder": "Where did the incident happen?",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "rows": 8,
                    "placeholder": (
                        "Please describe what happened..."
                    ),
                }
            ),

        }

    def clean(self):

        cleaned_data = super().clean()

        is_anonymous = cleaned_data.get(
            "is_anonymous"
        )

        if not is_anonymous:

            if not cleaned_data.get("complainant_name"):
                self.add_error(
                    "complainant_name",
                    "Please provide your name or choose anonymous reporting."
                )

        return cleaned_data