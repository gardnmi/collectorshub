from .models import Conversation, Message


def unread_message_count(request):
    if not request.user.is_authenticated:
        return {"unread_count": 0}
    conversations = Conversation.objects.filter(participants=request.user)
    unread_count = (
        Message.objects.filter(conversation__in=conversations, is_read=False)
        .exclude(sender=request.user)
        .count()
    )
    return {"unread_count": unread_count}
