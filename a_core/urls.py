from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from .views import index
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("a_accounts.urls")),
    path("collectibles/", include("a_collectibles.urls")),
    path("wishlist/", include("a_wishlist.urls")),
    path("messaging/", include(("a_messaging.urls", "messaging"), namespace="messaging")),
    path("", index, name="index"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
