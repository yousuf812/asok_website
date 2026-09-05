from django import forms

from .models import Donation


class DonationForm(forms.ModelForm):

    class Meta:
        model = Donation

        fields = [
            "donor_name",
            "email",
            "phone",
            "amount",
            "purpose",
            "payment_method",
            "transaction_id",
            "message",
        ]

        widgets = {
            "donor_name": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Your name",
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

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Enter donation amount",
                    "min": "1",
                    "step": "0.01",
                }
            ),

            "purpose": forms.Select(
                attrs={
                    "class": "form-input",
                }
            ),

            "payment_method": forms.Select(
                attrs={
                    "class": "form-input",
                }
            ),

            "transaction_id": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Enter transaction ID if available",
                }
            ),

            "message": forms.Textarea(
                attrs={
                    "class": "form-input",
                    "rows": 5,
                    "placeholder": "Optional message...",
                }
            ),
        }

        labels = {
            "donor_name": "Donor Name",
            "email": "Email Address",
            "phone": "Phone Number",
            "amount": "Donation Amount",
            "purpose": "Donation Purpose",
            "payment_method": "Payment Method",
            "transaction_id": "Transaction ID",
            "message": "Message",
        }

    def clean_donor_name(self):
        donor_name = self.cleaned_data["donor_name"].strip()

        if donor_name and len(donor_name) < 3:
            raise forms.ValidationError(
                "Please enter a valid name."
            )

        return donor_name

    def clean_amount(self):
        amount = self.cleaned_data["amount"]

        if amount <= 0:
            raise forms.ValidationError(
                "Donation amount must be greater than zero."
            )

        return amount

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()

        if phone and len(phone) < 8:
            raise forms.ValidationError(
                "Please enter a valid phone number."
            )

        return phone


class DonationLookupForm(forms.Form):

    reference_number = forms.CharField(
        max_length=25,
        label="Donation Reference Number",
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "Example: ASOK-D-1234ABCD",
            }
        ),
    )

    def clean_reference_number(self):
        reference_number = (
            self.cleaned_data["reference_number"]
            .strip()
            .upper()
        )

        if not reference_number.startswith("ASOK-D-"):
            raise forms.ValidationError(
                "Please enter a valid ASOK donation reference number."
            )

        return reference_number