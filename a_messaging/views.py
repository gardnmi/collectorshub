from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from .models import Conversation, Message
from a_collectibles.models import Collectible
from a_wishlist.models import WishlistItem
from django.contrib.auth import get_user_model
from .forms import MessageForm
from django.contrib import messages

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
        last_msg = convo.messages.order_by("-created_at").first() # type: ignore
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
    request: HttpRequest, pk: int | None = None, item_id: int | None = None
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
    # Wishlist offer support
    collectibles = conversation.collectibles.all() if conversation.collectibles.exists() else None
    collectibles_total = sum(c.price for c in collectibles) if collectibles else None
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
            "collectibles": collectibles,
            "collectibles_total": collectibles_total,
        },
    )


@login_required
def conversation_by_wishlist(request):
    # Assume the site owner/admin is the seller (first superuser)
    User = get_user_model()
    seller = User.objects.filter(is_superuser=True).first()
    if not seller:
        return HttpResponse("No admin/seller found.")
    wishlist_items = WishlistItem.objects.filter(user=request.user).select_related("collectible")
    if not wishlist_items:
        messages.warning(request, "Your wishlist is empty.")
        return redirect("wishlist")
    total = sum(item.collectible.price for item in wishlist_items)
    # Compose the wishlist summary
    summary = "Wishlist Offer:\n" + "\n".join([
        f"- {item.collectible.name} (${item.collectible.price})" for item in wishlist_items
    ]) + f"\nTotal: ${total:.2f}"
    # Create or get a conversation (no item, just participants)
    conversation, created = Conversation.objects.get_or_create(
        item=None,
    )
    conversation.participants.add(request.user, seller)
    # Link all wishlist collectibles to the conversation
    conversation.collectibles.set([item.collectible for item in wishlist_items])
    collectibles = conversation.collectibles.all()
    collectibles_total = sum(c.price for c in collectibles)
    messages_qs = Message.objects.filter(conversation=conversation).order_by("created_at")
    # If first message, pre-fill
    if request.method == "POST":
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.conversation = conversation
            msg.sender = request.user
            msg.text = form.cleaned_data["text"]
            msg.save()
            return redirect("a_messaging:conversation_detail", pk=conversation.pk)
    else:
        form = MessageForm()
    unread_count = get_unread_count(request.user)
    return render(
        request,
        "messaging/conversation_detail.html",
        {
            "conversation": conversation,
            "messages": messages_qs,
            "form": form,
            "unread_count": unread_count,
            "item": None,
            "collectibles": collectibles,
            "collectibles_total": collectibles_total,
        },
    )
