from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import Profile
from accounts.forms import UserUpdateForm, ProfileUpdateForm


# Create your views here.
@login_required
def profile(request):
    # Get the current user's profile
    user = request.user

    # Create or get profile (in case it doesn't exist yet)
    profile, created = Profile.objects.get_or_create(user=user)

    # Get user's collectibles
    collectibles = user.collectibles.all()

    # Import WishlistItem model using getattr to avoid circular import issues
    WishlistItem = getattr(
        __import__("wishlist.models", fromlist=["WishlistItem"]), "WishlistItem"
    )

    # Get user's wishlist items (prefetch related collectibles for efficiency)
    wishlist_items = WishlistItem.objects.filter(user=user).select_related(
        "collectible"
    )

    context = {
        "user": user,
        "profile": profile,
        "collectibles": collectibles,
        "wishlist_items": wishlist_items,
    }

    return render(request, "accounts/profile.html", context)


@login_required
def profile_edit(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form, "p_form": p_form, "profile": request.user.profile}

    return render(request, "accounts/profile_edit.html", context)
