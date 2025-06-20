from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "email": forms.EmailInput(attrs={"class": "input input-bordered w-full"}),
            "first_name": forms.TextInput(
                attrs={"class": "input input-bordered w-full"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "input input-bordered w-full"}
            ),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "location", "birth_date", "profile_image"]
        widgets = {
            "bio": forms.Textarea(
                attrs={"class": "textarea textarea-bordered w-full", "rows": 3}
            ),
            "location": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "birth_date": forms.DateInput(
                attrs={"type": "date", "class": "input input-bordered w-full"}
            ),
            "profile_image": forms.FileInput(
                attrs={"class": "file-input file-input-bordered w-full"}
            ),
        }
