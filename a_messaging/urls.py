from django.urls import path
from . import views

app_name = "messaging"

urlpatterns = [
    path("", views.inbox, name="inbox"),
    path(
        "conversation/<int:pk>/", views.conversation_detail, name="conversation_detail"
    ),
    path(
        "conversation/item/<int:item_id>/",
        views.conversation_detail,
        name="conversation_by_item",
    ),
]
