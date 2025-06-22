from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["text", "attachment", "offer_amount"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full resize-y",
                    "placeholder": "Type your message...",
                    "rows": 2,
                    "maxlength": 1000,
                }
            ),
            "attachment": forms.ClearableFileInput(
                attrs={"class": "file-input file-input-bordered"}
            ),
            "offer_amount": forms.NumberInput(
                attrs={
                    "class": "input input-bordered",
                    "placeholder": "Offer Amount",
                    "step": "0.01",
                    "min": "0",
                }
            ),
        }

    def clean_text(self):
        text = self.cleaned_data.get("text", "")
        if len(text) > 1000:
            raise forms.ValidationError("Messages cannot exceed 1000 characters.")
        return text
