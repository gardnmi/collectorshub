from django import template
from a_wishlist.models import WishlistItem

register = template.Library()

@register.filter
def in_wishlist(collectible, user):
    """Return True if the collectible is in the user's wishlist."""
    if not user.is_authenticated:
        return False
    return WishlistItem.objects.filter(user=user, collectible=collectible).exists()
