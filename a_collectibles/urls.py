from django.urls import path
from . import views

urlpatterns = [
    path("", views.collectible_list, name="collectible_list"),
    path("new/", views.collectible_create, name="collectible_create"),
    path("<int:pk>/", views.collectible_detail, name="collectible_detail"),
    path("<int:pk>/edit/", views.collectible_update, name="collectible_update"),
    path("<int:pk>/delete/", views.collectible_delete, name="collectible_delete"),
    # New AI enhancement endpoints
    path("<int:pk>/enhance-with-ai/", views.enhance_with_ai, name="enhance_with_ai"),
    path("<int:pk>/save-enhanced/", views.save_enhanced, name="save_enhanced"),
]
