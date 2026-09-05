from django import forms

from .models import LegalAidRequest


class LegalAidRequestForm(forms.ModelForm):

    class Meta:
        model = LegalAidRequest

        fields = [
            "full_name",
            "email",
            "phone",
            "category",
            "subject",
            "description",
            "preferred_contact",
        ]

        widgets = {

            "full_name": forms.TextInput(
                attrs={
                    "placeholder": "Your full name",
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

            "category": forms.Select(),

            "subject": forms.TextInput(
                attrs={
                    "placeholder": "Briefly describe your legal issue",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "placeholder": (
                        "Please explain your situation "
                        "and how we may help you..."
                    ),
                    "rows": 7,
                }
            ),

            "preferred_contact": forms.Select(),
        }