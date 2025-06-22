from django.contrib import admin
from .models import WishlistItem
from unfold.admin import ModelAdmin


# Register your models here.
@admin.register(WishlistItem)
class WishlistItemAdmin(ModelAdmin):
    list_display = ("user", "collectible", "added_on")
    list_filter = ("user", "added_on")
    search_fields = ("user__username", "collectible__name", "notes")
    date_hierarchy = "added_on"
