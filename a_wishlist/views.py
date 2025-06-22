from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string

from .models import WishlistItem
from a_collectibles.models import Collectible


# Create your views here.
@login_required
def wishlist(request):
    """Display the user's wishlist"""
    wishlist_items = WishlistItem.objects.filter(user=request.user).select_related(
        "collectible"
    )

    context = {
        "wishlist_items": wishlist_items,
    }

    return render(request, "wishlist/wishlist.html", context)


@require_POST
@login_required
def add_to_wishlist(request, pk):
    """Add an item to the user's wishlist"""
    collectible = get_object_or_404(Collectible, pk=pk)

    # Don't add to wishlist if user is the owner
    if collectible.owner == request.user:
        if request.headers.get("HX-Request"):
            return HttpResponse("You can't add your own items to your wishlist")
        messages.warning(request, "You can't add your own items to your wishlist")
        return redirect("collectible_detail", pk=pk)

    # Check if already in wishlist
    wishlist_item, created = WishlistItem.objects.get_or_create(
        user=request.user, collectible=collectible
    )

    if created:
        messages.success(request, "Added to wishlist!")
    else:
        messages.info(request, "Already in wishlist")

    # If it's an HTMX request, return updated button status
    if request.headers.get("HX-Request"):
        from django.template.loader import render_to_string

        # Render the wishlist button
        button_html = render_to_string(
            "wishlist/partials/wishlist_button.html",
            {"collectible": collectible, "in_wishlist": True},
            request=request,
        )

        # Render the messages
        messages_html = render_to_string(
            "partials/messages.html",
            {"messages": messages.get_messages(request), "htmx": True},
            request=request,
        )

        # Render the wishlist count with OOB swap
        count_html = render_to_string(
            "partials/wishlist_count.html", {"htmx": True}, request=request
        )

        # Combine all responses
        response = HttpResponse(button_html + messages_html + count_html)

        return response

    return redirect("collectible_detail", pk=pk)


@require_POST
@login_required
def remove_from_wishlist(request, pk):
    """Remove an item from the user's wishlist"""
    collectible = get_object_or_404(Collectible, pk=pk)

    try:
        wishlist_item = WishlistItem.objects.get(
            user=request.user, collectible=collectible
        )
        wishlist_item.delete()
        messages.success(request, "Removed from wishlist!")
    except WishlistItem.DoesNotExist:
        messages.warning(request, "Not in your wishlist")

    # If it's an HTMX request from collectible detail page, return updated button
    if request.headers.get("HX-Request") and request.headers.get(
        "HX-Current-URL", ""
    ).endswith(f"/collectibles/{pk}/"):
        # Render the wishlist button
        button_html = render_to_string(
            "wishlist/partials/wishlist_button.html",
            {"collectible": collectible, "in_wishlist": False},
            request=request,
        )

        # Render the messages
        messages_html = render_to_string(
            "partials/messages.html",
            {"messages": messages.get_messages(request), "htmx": True},
            request=request,
        )

        # Render the wishlist count with OOB swap
        count_html = render_to_string(
            "partials/wishlist_count.html", {"htmx": True}, request=request
        )

        # Combine all responses
        response = HttpResponse(button_html + messages_html + count_html)

        return response

    # If it's an HTMX request, always return the updated button
    if request.headers.get("HX-Request"):
        # Render the wishlist button for the wishlist page (after removal)
        button_html = render_to_string(
            "wishlist/partials/wishlist_button.html",
            {"collectible": collectible, "in_wishlist": False},
            request=request,
        )
        count_html = render_to_string(
            "partials/wishlist_count.html", {"htmx": True}, request=request
        )
        # Return both the button and the OOB wishlist count update
        return HttpResponse(button_html + count_html)

    # Otherwise redirect
    if "wishlist" in request.META.get("HTTP_REFERER", ""):
        return redirect("wishlist")
    return redirect("collectible_detail", pk=pk)


@login_required
def get_wishlist_count(request):
    """Get the current count of items in the user's wishlist - for AJAX requests"""
    count = WishlistItem.objects.filter(user=request.user).count()
    return JsonResponse({"count": count})


@login_required
def update_wishlist_count(request):
    """Return the updated wishlist count for HTMX requests"""
    return render(request, "partials/wishlist_count.html")
