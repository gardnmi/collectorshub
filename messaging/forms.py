from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text', 'attachment', 'is_offer', 'offer_amount']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full resize-y', 'placeholder': 'Type your message...', 'rows': 2}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'file-input file-input-bordered'}),
            'is_offer': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'offer_amount': forms.NumberInput(attrs={'class': 'input input-bordered', 'placeholder': 'Offer amount'}),
        }
