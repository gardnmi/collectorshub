from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin

from collectibles.models import Collectible, Category

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    # list_display = [field.name for field in User._meta.fields]


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


@admin.register(Collectible)
class CollectibleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "price",
        "condition",
        "is_sold",
        "get_categories",
        "created_at",
    ) # type: ignore
    list_filter = ("condition", "is_sold", "categories")
    search_fields = ("name", "description", "owner__username")

    def get_categories(self, obj):
        return ", ".join([category.display_name for category in obj.categories.all()])

    get_categories.short_description = "Categories"  # type: ignore


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("name", "display_name")
