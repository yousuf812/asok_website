from django import forms

from .models import MembershipApplication


class MembershipApplicationForm(forms.ModelForm):

    class Meta:
        model = MembershipApplication

        fields = [
            "full_name",
            "father_name",
            "mother_name",
            "email",
            "phone",
            "membership_type",
            "profession",
            "address",
            "nid_number",
            "birth_registration_number",
            "photo",
            "identity_document",
            "area_of_interest",
            "motivation",
        ]

        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "w-full rounded-lg border border-gray-300 px-4 py-3",
                    "placeholder": "Full Name",
                }
            ),

            "father_name": forms.TextInput(
                attrs={
                    "class": "w-full rounded-lg border border-gray-300 px-4 py-3",
                    "placeholder": "Father's Name",
                }
            ),

            "mother_name": forms.TextInput(
                attrs={
                    "class": "w-full rounded-lg border border-gray-300 px-4 py-3",
                    "placeholder": "Mother's Name",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "w-full rounded-lg border border-gray-300 px-4 py-3",
                    "placeholder": "Email Address",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "w-full rounded-lg border border-gray-300 px-4 py-3",
                    "placeholder": "Phone Number",
                }
            ),

            "membership_type": forms.Select(
                attrs={
                    "class": "w-full rounded-lg border border-gray-300 px-4 py-3"
                }
            ),

            "profession": forms.TextInput(
                attrs={
                    "class": "w-full rounded-lg border border-gray-300 px-4 py-3",
                    "placeholder": "Profession",
                }
            ),

            "address": forms.TextInput(
                attrs={
                    "class": "w-full rounded-lg border border-gray-300 px-4 py-3",
                    "placeholder": "Full Address",
                }
            ),

            "nid_number": forms.TextInput(
                attrs={
                    "class": "w-full rounded-lg border border-gray-300 px-4 py-3",
                    "placeholder": "NID Number",
                }
            ),

            "birth_registration_number": forms.TextInput(
                attrs={
                    "class": "w-full rounded-lg border border-gray-300 px-4 py-3",
                    "placeholder": "Birth Registration Number",
                }
            ),

            "photo": forms.ClearableFileInput(
                attrs={
                    "class": "w-full rounded-lg border border-gray-300 px-4 py-3",
                    "accept": "image/jpeg,image/png,image/webp",
                }
            ),

            "identity_document": forms.ClearableFileInput(
                attrs={
                    "class": "w-full rounded-lg border border-gray-300 px-4 py-3",
                    "accept": "image/jpeg,image/png,image/webp",
                }
            ),

            "area_of_interest": forms.Select(
                attrs={
                    "class": "w-full rounded-lg border border-gray-300 px-4 py-3"
                }
            ),

            "motivation": forms.Textarea(
                attrs={
                    "class": "w-full rounded-lg border border-gray-300 px-4 py-3",
                    "rows": 5,
                    "placeholder": "Why do you want to join ASOK Foundation?",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        nid_number = cleaned_data.get("nid_number")
        birth_registration_number = cleaned_data.get(
            "birth_registration_number"
        )

        if not nid_number and not birth_registration_number:
            raise forms.ValidationError(
                "Please provide either NID Number or Birth Registration Number."
            )

        return cleaned_data

    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name", "").strip()

        if not full_name:
            raise forms.ValidationError(
                "Full name is required."
            )

        return full_name

    def clean_father_name(self):
        father_name = self.cleaned_data.get("father_name", "").strip()

        if not father_name:
            raise forms.ValidationError(
                "Father's name is required."
            )

        return father_name

    def clean_mother_name(self):
        mother_name = self.cleaned_data.get("mother_name", "").strip()

        if not mother_name:
            raise forms.ValidationError(
                "Mother's name is required."
            )

        return mother_name

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()

        if not phone:
            raise forms.ValidationError(
                "Phone number is required."
            )

        return phone

    def clean_photo(self):
        photo = self.cleaned_data.get("photo")

        if not photo:
            raise forms.ValidationError(
                "Member photo is required."
            )

        allowed_types = [
            "image/jpeg",
            "image/png",
            "image/webp",
        ]

        if photo.content_type not in allowed_types:
            raise forms.ValidationError(
                "Only JPG, PNG or WEBP images are allowed."
            )

        if photo.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                "Photo size must not exceed 5 MB."
            )

        return photo

    def clean_identity_document(self):
        document = self.cleaned_data.get("identity_document")

        if not document:
            raise forms.ValidationError(
                "NID or Birth Registration document image is required."
            )

        allowed_types = [
            "image/jpeg",
            "image/png",
            "image/webp",
        ]

        if document.content_type not in allowed_types:
            raise forms.ValidationError(
                "Only JPG, PNG or WEBP images are allowed."
            )

        if document.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                "Identity document image size must not exceed 5 MB."
            )

        return document






from .models import MembershipPayment


class MemberMonthlyPaymentForm(forms.ModelForm):

    class Meta:
        model = MembershipPayment

        fields = [
            "amount",
            "payment_method",
            "payment_month",
            "transaction_id",
            "notes",
        ]

        widgets = {
            "amount": forms.NumberInput(
                attrs={
                    "class": (
                        "w-full rounded-xl border border-slate-300 "
                        "px-4 py-3 outline-none "
                        "focus:border-emerald-600 "
                        "focus:ring-2 focus:ring-emerald-100"
                    ),
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "payment_method": forms.Select(
                attrs={
                    "class": (
                        "w-full rounded-xl border border-slate-300 "
                        "px-4 py-3 outline-none "
                        "focus:border-emerald-600 "
                        "focus:ring-2 focus:ring-emerald-100"
                    ),
                }
            ),

            "payment_month": forms.DateInput(
                attrs={
                    "type": "month",
                    "class": (
                        "w-full rounded-xl border border-slate-300 "
                        "px-4 py-3 outline-none "
                        "focus:border-emerald-600 "
                        "focus:ring-2 focus:ring-emerald-100"
                    ),
                }
            ),

            "transaction_id": forms.TextInput(
                attrs={
                    "class": (
                        "w-full rounded-xl border border-slate-300 "
                        "px-4 py-3 outline-none "
                        "focus:border-emerald-600 "
                        "focus:ring-2 focus:ring-emerald-100"
                    ),
                    "placeholder": "bKash / Nagad / Bank Transaction ID",
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": (
                        "w-full rounded-xl border border-slate-300 "
                        "px-4 py-3 outline-none "
                        "focus:border-emerald-600 "
                        "focus:ring-2 focus:ring-emerald-100"
                    ),
                    "rows": 3,
                    "placeholder": "Optional notes",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["payment_method"].choices = [
            choice
            for choice in self.fields["payment_method"].choices
            if choice[0] != ""
        ]

    def clean_payment_month(self):
        payment_month = self.cleaned_data["payment_month"]

        if payment_month:
            # Store the first day of the selected month.
            return payment_month.replace(day=1)

        return payment_month