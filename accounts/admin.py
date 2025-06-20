from django.contrib import admin
from accounts.models import Profile

from unfold.admin import ModelAdmin


admin.site.unregister(Profile)  # Unregister the default Profile admin if it exists

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ('user', 'location', 'birth_date')
    search_fields = ('user__username', 'location')
