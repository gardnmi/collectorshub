from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from collectorshub.views import index
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("accounts.urls")),
    path("collectibles/", include("collectibles.urls")),
    path("wishlist/", include("wishlist.urls")),
    path("messaging/", include(("messaging.urls", "messaging"), namespace="messaging")),
    path("", index, name="index"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
