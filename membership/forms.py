from django import forms

from .models import MembershipApplication


class MembershipApplicationForm(forms.ModelForm):

    class Meta:
        model = MembershipApplication

        fields = [
            "full_name",
            "email",
            "phone",
            "membership_type",
            "profession",
            "address",
            "area_of_interest",
            "motivation",
        ]

        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Enter your full name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "you@example.com",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "+880 1XXXXXXXXX",
                }
            ),
            "membership_type": forms.Select(
                attrs={
                    "class": "form-input",
                }
            ),
            "profession": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Student, Teacher, Lawyer, Business etc.",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Your current address",
                }
            ),
            "area_of_interest": forms.Select(
                attrs={
                    "class": "form-input",
                }
            ),
            "motivation": forms.Textarea(
                attrs={
                    "class": "form-input",
                    "rows": 6,
                    "placeholder": "Tell us why you want to join ASOK Foundation...",
                }
            ),
        }

        labels = {
            "full_name": "Full Name",
            "email": "Email Address",
            "phone": "Phone Number",
            "membership_type": "Membership Type",
            "profession": "Profession",
            "address": "Address",
            "area_of_interest": "Area of Interest",
            "motivation": "Why do you want to join?",
        }

    def clean_full_name(self):
        full_name = self.cleaned_data["full_name"].strip()

        if len(full_name) < 3:
            raise forms.ValidationError(
                "Please enter your full name."
            )

        return full_name

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()

        if len(phone) < 8:
            raise forms.ValidationError(
                "Please enter a valid phone number."
            )

        return phone

    def clean_motivation(self):
        motivation = self.cleaned_data["motivation"].strip()

        if len(motivation) < 20:
            raise forms.ValidationError(
                "Please provide at least 20 characters explaining your motivation."
            )

        return motivation