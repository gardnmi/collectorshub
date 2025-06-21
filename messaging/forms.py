from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text', 'attachment', 'is_offer', 'offer_amount']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'input input-bordered grow', 'placeholder': 'Type your message...'}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'file-input file-input-bordered'}),
            'is_offer': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'offer_amount': forms.NumberInput(attrs={'class': 'input input-bordered', 'placeholder': 'Offer amount'}),
        }
