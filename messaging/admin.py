from django.contrib import admin
from .models import Conversation, Message

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'created_at', 'updated_at')
    search_fields = ('id', 'item__name')
    filter_horizontal = ('participants',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'sender', 'created_at', 'offer_amount', 'is_read')
    search_fields = ('conversation__id', 'sender__username', 'text')
    list_filter = ('is_read', 'created_at')
