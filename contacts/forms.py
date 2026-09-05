from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):

    class Meta:
        model = ContactMessage

        fields = [
            "full_name",
            "email",
            "phone",
            "subject",
            "message",
        ]

        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Your full name",
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

            "subject": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "How can we help you?",
                }
            ),

            "message": forms.Textarea(
                attrs={
                    "class": "form-input",
                    "rows": 6,
                    "placeholder": "Write your message...",
                }
            ),
        }

        labels = {
            "full_name": "Full Name",
            "email": "Email Address",
            "phone": "Phone Number",
            "subject": "Subject",
            "message": "Message",
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

        if phone and len(phone) < 8:
            raise forms.ValidationError(
                "Please enter a valid phone number."
            )

        return phone

    def clean_subject(self):
        subject = self.cleaned_data["subject"].strip()

        if len(subject) < 5:
            raise forms.ValidationError(
                "Subject must contain at least 5 characters."
            )

        return subject

    def clean_message(self):
        message = self.cleaned_data["message"].strip()

        if len(message) < 10:
            raise forms.ValidationError(
                "Please provide at least 10 characters in your message."
            )

        return message