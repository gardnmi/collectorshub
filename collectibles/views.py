import json

import llm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.conf import settings

from collectibles.forms import CollectibleForm, CollectibleImageFormSet, CollectibleImageForm
from .models import Collectible, CollectibleImage
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.conf import settings
from django.http import HttpResponse
from django.db.models import Prefetch
from django.forms import modelformset_factory

from collectibles.forms import CollectibleForm, CollectibleImageForm, CollectibleImageFormSet
from .models import Collectible, CollectibleImage

OPENAI_API_KEY = getattr(settings, "OPENAI_API_KEY")


# List all collectibles
def collectible_list(request):
    collectibles = Collectible.objects.filter(is_sold=False).order_by("-created_at")
    return render(
        request, "collectibles/collectible_list.html", {"collectibles": collectibles}
    )


# View a single collectible
@login_required
def collectible_detail(request, pk):
    collectible = get_object_or_404(
        Collectible.objects.prefetch_related('collectible_images'), pk=pk
    )

    # Check if item is in user's wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        # Using getattr to avoid import errors since this is a circular import
        WishlistItem = getattr(
            __import__("wishlist.models", fromlist=["WishlistItem"]), "WishlistItem"
        )
        in_wishlist = WishlistItem.objects.filter(
            user=request.user, collectible=collectible
        ).exists()

    return render(
        request,
        "collectibles/collectible_detail.html",
        {"collectible": collectible, "in_wishlist": in_wishlist},
    )


# Create a new collectible
@login_required
def collectible_create(request):
    if request.method == "POST":
        form = CollectibleForm(request.POST, request.FILES)
        formset = CollectibleImageFormSet(request.POST, request.FILES)
        
        # Check for forms marked for removal by JavaScript
        for image_form in formset:
            if hasattr(image_form, '_should_delete') and image_form._should_delete:
                image_form.instance._delete = True
        
        if form.is_valid() and formset.is_valid():
            collectible = form.save(commit=False)
            collectible.owner = request.user
            collectible.save()
            form.save_m2m()  # Save many-to-many relationships (categories)
            
            # Save the formset
            instances = formset.save(commit=False)
            for instance in instances:
                if not hasattr(instance, '_delete'):
                    instance.collectible = collectible
                    instance.save()
            
            # Handle legacy single image if provided
            if collectible.image and not collectible.collectible_images.exists():
                # Create a CollectibleImage from the legacy image field
                CollectibleImage.objects.create(
                    collectible=collectible,
                    image=collectible.image,
                    is_primary=True,
                    order=0
                )
                
            messages.success(request, "Collectible added successfully!")
            return redirect("collectible_detail", pk=collectible.pk)
    else:
        form = CollectibleForm()
        formset = CollectibleImageFormSet()
        
    return render(
        request,
        "collectibles/collectible_form.html",
        {"form": form, "formset": formset, "title": "List New Collectible"},
    )


# Update an existing collectible
@login_required
def collectible_update(request, pk):
    # Ensure only owner can update
    collectible = get_object_or_404(Collectible, pk=pk, owner=request.user)
    
    if request.method == "POST":
        form = CollectibleForm(request.POST, request.FILES, instance=collectible)
        formset = CollectibleImageFormSet(request.POST, request.FILES, instance=collectible)
        
        # Check for forms marked for removal by JavaScript
        for image_form in formset:
            if hasattr(image_form, '_should_delete') and image_form._should_delete:
                if not image_form.instance.pk:  # Only for new forms
                    image_form.instance._delete = True
        
        if form.is_valid() and formset.is_valid():
            form.save()
            
            # Process formset with special handling
            instances = formset.save(commit=False)
            for instance in instances:
                if not hasattr(instance, '_delete'):
                    instance.save()
                    
            # Process deletions marked by formset
            for obj in formset.deleted_objects:
                obj.delete()
            
            # If a new primary image was selected, update all other images to not be primary
            primary_images = collectible.collectible_images.filter(is_primary=True)
            if primary_images.count() > 1:
                # Keep only the last one as primary
                primary = primary_images.last()
                primary_images.exclude(pk=primary.pk).update(is_primary=False)
                
            messages.success(request, "Collectible updated successfully!")
            return redirect("collectible_detail", pk=collectible.pk)
    else:
        form = CollectibleForm(instance=collectible)
        formset = CollectibleImageFormSet(instance=collectible)
        
    return render(
        request,
        "collectibles/collectible_form.html",
        {"form": form, "formset": formset, "title": "Update Collectible"},
    )


@login_required
def collectible_delete(request, pk):
    # Ensure only owner can delete
    collectible = get_object_or_404(Collectible, pk=pk, owner=request.user)
    if request.method == "POST":
        collectible.delete()
        messages.success(request, "Collectible deleted successfully!")
        return redirect("collectible_list")
    return render(
        request,
        "collectibles/collectible_confirm_delete.html",
        {"collectible": collectible},
    )


@login_required
def enhance_with_ai(request, pk):
    # Ensure only owner can enhance
    collectible = get_object_or_404(Collectible, pk=pk, owner=request.user)

    # Mock AI enhancement (similar to improve_collectible_description_ai)
    try:
        # Create a mock response or call the LLM service
        mock_response = False  # Set to False to use actual LLM

        if mock_response:
            # Mock improved response
            enhanced = {
                "name": "Mock AI Enhanced Name",
                "description": ("Mocka AI Enhanced Description."),
            }
        else:
            # Here you would call the LLM service with a prompt
            prompt = """
                You are an expert e-commerce copywriter and market analyst specializing in collectible items.
                Your task is to improve a collectible listing's name and description for an eBay-like marketplace.

                Focus on making the description more engaging, detailed, professional, and appealing to potential buyers.
                Highlight key features and benefits, and use clear, concise language.

                Please return the improved name, description, and a suggested price in JSON format with the keys 'name' and 'description'

                I will also provide an image of the collectible to help you improve the name and description.

                Example format:
                {
                    "name": "Improved Name Here",
                    "description": "Improved, detailed description here.",
                }
                """

            # Get the primary image or fall back to the legacy image field
            image_to_use = None
            if collectible.primary_image:
                image_to_use = collectible.primary_image.image.path
            elif collectible.image:
                image_to_use = collectible.image.path
            
            model = llm.get_model("gpt-4.1-nano")

            llm_response = model.prompt(
                prompt=prompt,
                schema={
                    "properties": {
                        "name": {"title": "Name", "type": "string"},
                        "description": {"title": "Description", "type": "string"},
                    },
                    "required": ["name", "description"],
                    "title": "CollectibleItem",
                    "type": "object",
                },
                attachments=[llm.Attachment(path=image_to_use)] if image_to_use else [],
                key=OPENAI_API_KEY,
            ).json()

            content = json.loads(llm_response["content"])  # type: ignore

            enhanced = {
                "name": content.get("name", collectible.name),
                "description": content.get("description", collectible.description),
            }

        # Pass the original and enhanced data to the template
        original = {
            "name": collectible.name,
            "description": collectible.description,
        }

        return render(
            request,
            "collectibles/collectible_enhanced.html",
            {"collectible": collectible, "original": original, "enhanced": enhanced},
        )

    except Exception as e:
        print(f"AI Enhancement Error: {e}")
        messages.error(request, f"An error occurred during AI enhancement: {str(e)}")
        return redirect("collectible_detail", pk=pk)


@login_required
@require_POST
def save_enhanced(request, pk):
    # Ensure only owner can save enhanced version
    collectible = get_object_or_404(Collectible, pk=pk, owner=request.user)

    try:
        # Get the enhanced data from the form
        name = request.POST.get("name")
        description = request.POST.get("description")

        # Update the collectible
        collectible.name = name
        collectible.description = description
        collectible.save()

        messages.success(request, "Enhanced collectible saved successfully!")
        return redirect("collectible_detail", pk=pk)

    except Exception as e:
        print(f"Save Enhanced Error: {e}")
        messages.error(
            request,
            f"An error occurred while saving the enhanced collectible: {str(e)}",
        )
        return redirect("collectible_detail", pk=pk)


def image_detail(request, pk, image_pk):
    """View a single image from a collectible."""
    collectible = get_object_or_404(Collectible, pk=pk)
    image = get_object_or_404(CollectibleImage, pk=image_pk, collectible=collectible)
    
    # Get all images for this collectible to determine next/previous
    images = list(collectible.collectible_images.all())
    current_index = next((i for i, img in enumerate(images) if img.pk == image_pk), 0)
    
    # Get previous and next images
    previous_image = images[current_index - 1] if current_index > 0 else None
    next_image = images[current_index + 1] if current_index < len(images) - 1 else None
    
    return render(
        request,
        "collectibles/partials/image_detail.html",
        {
            "collectible": collectible, 
            "image": image,
            "previous_image": previous_image,
            "next_image": next_image,
            "forloop": {"first": current_index == 0, "last": current_index == len(images) - 1}
        },
    )


@login_required
def collectible_add_image_form(request):
    """Return a form for adding a new collectible image via HTMX."""
    form = CollectibleImageForm(prefix=f"collectible_images-{request.GET.get('index', 'new')}")
    return render(
        request,
        "collectibles/partials/image_form.html",
        {"form": form},
    )
