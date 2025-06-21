from django.contrib import admin
from accounts.models import Profile

from unfold.admin import ModelAdmin


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ("user", "location", "birth_date") # type: ignore
    search_fields = ("user__username", "location")
