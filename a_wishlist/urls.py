from django.urls import path
from . import views

urlpatterns = [
    path("", views.wishlist, name="wishlist"),
    path("add/<int:pk>/", views.add_to_wishlist, name="add_to_wishlist"),
    path("remove/<int:pk>/", views.remove_from_wishlist, name="remove_from_wishlist"),
    path("count/", views.get_wishlist_count, name="wishlist_count"),
    path("update-count/", views.update_wishlist_count, name="update_wishlist_count"),
]
