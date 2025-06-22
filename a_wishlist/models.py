from django.db import models
from django.contrib.auth.models import User
from a_collectibles.models import Collectible


# Create your models here.
class WishlistItem(models.Model):
    """Model for wishlist items that users can add to their profile"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="wishlist_items"
    )
    collectible = models.ForeignKey(
        Collectible, on_delete=models.CASCADE, related_name="in_wishlists"
    )
    added_on = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(
        blank=True, null=True, help_text="Any notes about why you want this item"
    )

    class Meta:
        unique_together = ["user", "collectible"]  # Prevent duplicate wishlist items
        ordering = ["-added_on"]

    def __str__(self):
        return f"{self.user.username}'s wishlist: {self.collectible.name}"
