from django import forms
from .models import Collectible, CollectibleImage, Category
from typing import Any


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        base_attrs = {"class": "file-input file-input-bordered w-full"}
        if attrs:
            base_attrs.update(attrs)
        super().__init__(attrs=base_attrs)


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
    new_category = forms.CharField(
        required=False,
        label="Add New Category",
        help_text="If your category doesn't exist, add it here.",
        widget=forms.TextInput(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "New Category Name",
            }
        ),
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
        self.fields["categories"].required = False
        # You can add more customization here if needed

    def clean(self):
        cleaned_data = super().clean()
        new_category = cleaned_data.get("new_category")
        if new_category:
            category, created = Category.objects.get_or_create(
                name=new_category, defaults={"display_name": new_category}
            )
            # Add the new category to the categories field
            if "categories" in self.cleaned_data:
                self.cleaned_data["categories"] = list(
                    self.cleaned_data["categories"]
                ) + [category]
            else:
                self.cleaned_data["categories"] = [category]
        return cleaned_data


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
