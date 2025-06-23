from django import forms
from .models import WishlistOffer

class WishlistOfferForm(forms.ModelForm):
    class Meta:
        model = WishlistOffer
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4, "placeholder": "Add a message (optional)"}),
        }
