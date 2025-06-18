from django import forms
from collectibles.models import Collectible

class CollectibleForm(forms.ModelForm):
    class Meta:
        model = Collectible
        fields = ['name', 'description', 'price', 'condition', 'image', 'categories']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'Collectible Name'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'placeholder': 'Describe your collectible...', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'e.g., 99.99'}),
            'condition': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'image': forms.FileInput(attrs={'class': 'file-input file-input-bordered w-full'}),
            'categories': forms.SelectMultiple(attrs={'class': 'select select-bordered w-full', 'size': '5', 'style': 'height: auto; min-height: 8rem; resize: vertical;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You can add more customization here if needed
        # For example, if you want to add specific DaisyUI classes to certain fields