from django import forms
from collectibles.models import Collectible, CollectibleImage


class CollectibleForm(forms.ModelForm):
    class Meta:
        model = Collectible
        fields = ["name", "description", "price", "condition", "image", "categories"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Collectible Name",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "placeholder": "Describe your collectible...",
                    "rows": 4,
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "e.g., 99.99",
                }
            ),
            "condition": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "image": forms.FileInput(
                attrs={
                    "class": "file-input file-input-bordered w-full",
                    "help_text": "Legacy single image upload (use multi-image upload below if possible)",
                }
            ),
            "categories": forms.SelectMultiple(
                attrs={
                    "class": "select select-bordered w-full",
                    "size": "5",
                    "style": "height: auto; min-height: 8rem; resize: vertical;",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You can add more customization here if needed
        # For example, if you want to add specific DaisyUI classes to certain fields


class CollectibleImageForm(forms.ModelForm):
    """Form for handling multiple images for a collectible."""
    class Meta:
        model = CollectibleImage
        fields = ["image", "is_primary", "caption"]
        widgets = {
            "image": forms.FileInput(
                attrs={"class": "file-input file-input-bordered w-full"}
            ),
            "is_primary": forms.CheckboxInput(
                attrs={"class": "checkbox"}
            ),
            "caption": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Image caption (optional)",
                }
            ),
        }
    
    def clean_image(self):
        """Allow empty image fields for forms that will be removed by JavaScript."""
        image = self.cleaned_data.get('image')
        if not image and not self.instance.pk:
            # If this is a new form (not an existing image) and has no image,
            # mark it for removal but don't raise validation error
            self._should_delete = True
        return image


CollectibleImageFormSet = forms.inlineformset_factory(
    Collectible,
    CollectibleImage,
    form=CollectibleImageForm,
    extra=1,  # Start with one extra form
    max_num=5,  # Maximum of 5 images allowed
    can_delete=True,
    validate_max=True,
)
