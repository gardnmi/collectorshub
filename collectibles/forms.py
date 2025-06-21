from django import forms
from collectibles.models import Collectible, CollectibleImage
from typing import Any


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)] if data else []
        return result


class CollectibleForm(forms.ModelForm):
    images = MultipleFileField(
        required=False,
        label="Add Images",
        help_text="You can upload multiple images.",
    )

    class Meta:
        model = Collectible
        fields = ["name", "description", "price", "condition", "categories"]
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
            "categories": forms.SelectMultiple(
                attrs={
                    "class": "select select-bordered w-full",
                    "size": "5",
                    "style": "height: auto; min-height: 8rem; resize: vertical;",
                }
            ),
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        # You can add more customization here if needed
        # For example, if you want to add specific DaisyUI classes to certain fields


class CollectibleImageForm(forms.ModelForm):
    class Meta:
        model = CollectibleImage
        fields = ["image", "is_primary"]
        widgets = {
            "image": forms.ClearableFileInput(
                attrs={"class": "file-input file-input-bordered w-full"}
            ),
            "is_primary": forms.CheckboxInput(
                attrs={"class": "checkbox checkbox-primary"}
            ),
        }
