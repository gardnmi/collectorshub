from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string

from .models import WishlistItem
from .forms import WishlistOfferForm
from .models import WishlistOffer
from a_collectibles.models import Collectible


# Create your views here.
@login_required
def wishlist(request):
    """Display the user's wishlist"""
    wishlist_items = WishlistItem.objects.filter(user=request.user).select_related(
        "collectible"
    )
    wishlist_total = sum(item.collectible.price for item in wishlist_items)
    context = {
        "wishlist_items": wishlist_items,
        "wishlist_total": wishlist_total,
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


@login_required
def wishlist_offer_create(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user).select_related("collectible")
    if not wishlist_items:
        messages.warning(request, "Your wishlist is empty.")
        return redirect("wishlist")
    total = sum(item.collectible.price for item in wishlist_items)
    if request.method == "POST":
        form = WishlistOfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.user = request.user
            offer.total_amount = total
            offer.save()
            offer.items.set([item.collectible for item in wishlist_items])
            messages.success(request, "Your offer for the entire wishlist has been submitted!")
            return redirect("wishlist")
    else:
        form = WishlistOfferForm()
    return render(request, "wishlist/wishlist_offer_form.html", {
        "form": form,
        "wishlist_items": wishlist_items,
        "wishlist_total": total,
    })
