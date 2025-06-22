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
    return Message.objects.filter(conversation__in=conversations, is_read=False).exclude(sender=user).count()

@login_required
def inbox(request: HttpRequest) -> HttpResponse:
    conversations = request.user.conversations.order_by('-updated_at')
    unread_count = get_unread_count(request.user)
    return render(request, 'messaging/inbox.html', {'conversations': conversations, 'unread_count': unread_count})

@login_required
def conversation_detail(request: HttpRequest, pk: int) -> HttpResponse:
    conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)
    messages = Message.objects.filter(conversation=conversation).select_related('sender').order_by('created_at')
    Message.objects.filter(conversation=conversation, is_read=False).exclude(sender=request.user).update(is_read=True)
    unread_count = get_unread_count(request.user)
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.conversation = conversation
            msg.sender = request.user
            msg.save()
            return redirect('messaging:conversation_detail', pk=pk)
    else:
        form = MessageForm()
    return render(request, 'messaging/conversation_detail.html', {'conversation': conversation, 'messages': messages, 'form': form, 'unread_count': unread_count})

@login_required
def start_conversation(request: HttpRequest, item_id: int = None) -> HttpResponse:
    item = None
    seller = None
    if item_id:
        item = get_object_or_404(Collectible, pk=item_id)
        seller = item.owner
    if request.method == 'POST':
        if item and seller:
            conversation, created = Conversation.objects.get_or_create(
                item=item,
            )
            conversation.participants.add(request.user, seller)
            return redirect('messaging:conversation_detail', pk=conversation.pk)
        else:
            other_user_id = request.POST.get('user_id')
            other_user = get_object_or_404(User, pk=other_user_id)
            conversation, created = Conversation.objects.get_or_create()
            conversation.participants.add(request.user, other_user)
            return redirect('messaging:conversation_detail', pk=conversation.pk)
    unread_count = get_unread_count(request.user)
    return render(request, 'messaging/start_conversation.html', {'item': item, 'seller': seller, 'unread_count': unread_count})
