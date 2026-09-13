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
            "nid_number",
            "birth_registration_number",
            "photo",
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

            "nid_number": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Enter your NID number",
                }
            ),

            "birth_registration_number": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Enter your Birth Registration number",
                }
            ),

            "photo": forms.ClearableFileInput(
                attrs={
                    "class": "form-input",
                    "accept": "image/jpeg,image/png,image/webp",
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
                    "placeholder": (
                        "Tell us why you want to join ASOK Foundation..."
                    ),
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
            "nid_number": "NID Number",
            "birth_registration_number": "Birth Registration Number",
            "photo": "Member Photo",
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

    def clean(self):
        cleaned_data = super().clean()

        nid_number = (
            cleaned_data.get("nid_number") or ""
        ).strip()

        birth_registration_number = (
            cleaned_data.get("birth_registration_number") or ""
        ).strip()

        if not nid_number and not birth_registration_number:
            raise forms.ValidationError(
                "Please provide either your NID number "
                "or Birth Registration number."
            )

        return cleaned_data

    def clean_photo(self):
        photo = self.cleaned_data.get("photo")

        if not photo:
            raise forms.ValidationError(
                "Please upload your recent photo."
            )

        allowed_types = [
            "image/jpeg",
            "image/png",
            "image/webp",
        ]

        if photo.content_type not in allowed_types:
            raise forms.ValidationError(
                "Please upload a JPG, PNG, or WebP image."
            )

        if photo.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                "Photo size must not exceed 5 MB."
            )

        return photo

    def clean_motivation(self):
        motivation = self.cleaned_data["motivation"].strip()

        if len(motivation) < 20:
            raise forms.ValidationError(
                "Please provide at least 20 characters "
                "explaining your motivation."
            )

        return motivation