from django.db import models
from django.contrib.auth import get_user_model
from a_collectibles.models import Collectible

User = get_user_model()


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name="conversations")
    item = models.ForeignKey(
        Collectible,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="conversations",
    )
    collectibles = models.ManyToManyField(
        Collectible,
        blank=True,
        related_name="multi_conversations"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.item:
            return f"Conversation about {self.item.name} ({self.pk})"
        elif self.collectibles.exists():
            return f"Conversation about {self.collectibles.count()} items (#{self.pk})"
        return f"Conversation #{self.pk}"


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    text = models.TextField(blank=True)
    attachment = models.FileField(
        upload_to="message_attachments/", blank=True, null=True
    )
    offer_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} in Conversation {self.conversation.pk}"
