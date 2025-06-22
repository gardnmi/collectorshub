from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from .models import Conversation, Message
from collectibles.models import Collectible
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse
from .forms import MessageForm

User = get_user_model()

@login_required
def inbox(request: HttpRequest) -> HttpResponse:
    conversations = request.user.conversations.order_by('-updated_at')
    return render(request, 'messaging/inbox.html', {'conversations': conversations})

@login_required
def conversation_detail(request: HttpRequest, pk: int) -> HttpResponse:
    conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)
    messages = conversation.messages.select_related('sender').order_by('created_at')
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.conversation = conversation
            msg.sender = request.user
            msg.save()
            if request.headers.get('HX-Request'):
                messages_html = render_to_string('messaging/_messages_list.html', {'messages': Message.objects.filter(conversation=conversation).select_related('sender').order_by('created_at'), 'user': request.user})
                form_html = render_to_string('messaging/_message_form.html', {'form': MessageForm(), 'user': request.user, 'conversation': conversation})
                return HttpResponse(messages_html + form_html)
            return redirect('messaging:conversation_detail', pk=pk)
    else:
        form = MessageForm()
    return render(request, 'messaging/conversation_detail.html', {'conversation': conversation, 'messages': messages, 'form': form})

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
    return render(request, 'messaging/start_conversation.html', {'item': item, 'seller': seller})
