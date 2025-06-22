from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from .models import Conversation, Message
from collectibles.models import Collectible
from django.contrib.auth import get_user_model
from .forms import MessageForm

User = get_user_model()


def get_unread_count(user):
    if not user.is_authenticated:
        return 0
    conversations = Conversation.objects.filter(participants=user)
    return (
        Message.objects.filter(conversation__in=conversations, is_read=False)
        .exclude(sender=user)
        .count()
    )


@login_required
def inbox(request: HttpRequest) -> HttpResponse:
    conversations = Conversation.objects.filter(participants=request.user)
    # Annotate each conversation with unread count for this user
    convo_list = []
    for convo in conversations:
        unread = (
            Message.objects.filter(conversation=convo, is_read=False)
            .exclude(sender=request.user)
            .exists()
        )
        last_msg = convo.messages.order_by("-created_at").first()
        convo_list.append(
            {
                "convo": convo,
                "unread": unread,
                "last_updated": last_msg.created_at if last_msg else convo.updated_at,
            }
        )
    # Sort: unread first, then by last updated
    convo_list.sort(key=lambda c: (not c["unread"], -c["last_updated"].timestamp()))
    unread_count = get_unread_count(request.user)
    return render(
        request,
        "messaging/inbox.html",
        {"convo_list": convo_list, "unread_count": unread_count},
    )


@login_required
def conversation_detail(
    request: HttpRequest, pk: int = None, item_id: int = None
) -> HttpResponse:
    if item_id:
        item = get_object_or_404(Collectible, pk=item_id)
        seller = item.owner
        # Get or create conversation for this item and these two users
        conversation, created = Conversation.objects.get_or_create(item=item)
        conversation.participants.add(request.user, seller)
    else:
        conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)
        item = conversation.item if conversation.item else None
    messages = (
        Message.objects.filter(conversation=conversation)
        .select_related("sender")
        .order_by("created_at")
    )
    Message.objects.filter(conversation=conversation, is_read=False).exclude(
        sender=request.user
    ).update(is_read=True)
    unread_count = get_unread_count(request.user)
    if request.method == "POST":
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.conversation = conversation
            msg.sender = request.user
            msg.save()
            return redirect("messaging:conversation_detail", pk=conversation.pk)
    else:
        form = MessageForm()
    return render(
        request,
        "messaging/conversation_detail.html",
        {
            "conversation": conversation,
            "messages": messages,
            "form": form,
            "unread_count": unread_count,
            "item": item,
        },
    )
