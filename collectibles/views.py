import json

import llm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.conf import settings

from collectibles.forms import CollectibleForm

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
    collectible = get_object_or_404(Collectible, pk=pk)

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

    # Get the primary image (or first image if none marked primary)
    images = collectible.images.all()
    primary_image = images.filter(is_primary=True).first() or images.first()

    return render(
        request,
        "collectibles/collectible_detail.html",
        {
            "collectible": collectible,
            "in_wishlist": in_wishlist,
            "primary_image": primary_image,
            "images": images,
        },
    )


# Create a new collectible
@login_required
def collectible_create(request):
    if request.method == "POST":
        form = CollectibleForm(request.POST, request.FILES)
        if form.is_valid():
            collectible = form.save(commit=False)
            collectible.owner = request.user
            collectible.save()
            form.save_m2m()
            # Handle multiple images
            images = request.FILES.getlist("images")
            for idx, image in enumerate(images):
                CollectibleImage.objects.create(
                    collectible=collectible,
                    image=image,
                    is_primary=(idx == 0),  # First image is primary by default
                )
            messages.success(request, "Collectible added successfully!")
            return redirect("collectible_detail", pk=collectible.pk)
    else:
        form = CollectibleForm()
    return render(
        request,
        "collectibles/collectible_form.html",
        {"form": form, "title": "List New Collectible"},
    )


# Update an existing collectible
@login_required
def collectible_update(request, pk):
    collectible = get_object_or_404(Collectible, pk=pk, owner=request.user)
    images = collectible.images.all()  # This is valid after model edit
    if request.method == "POST":
        form = CollectibleForm(request.POST, request.FILES, instance=collectible)
        if form.is_valid():
            form.save()
            # Handle new images
            new_images = request.FILES.getlist("images")
            for image in new_images:
                CollectibleImage.objects.create(
                    collectible=collectible,
                    image=image,
                    is_primary=False,
                )
            # Handle image actions (delete, set primary)
            for img in images:
                if f"delete_image_{img.id}" in request.POST:
                    img.delete()
                elif f"set_primary_{img.id}" in request.POST:
                    images.update(is_primary=False)
                    img.is_primary = True
                    img.save()
            messages.success(request, "Collectible updated successfully!")
            return redirect("collectible_detail", pk=collectible.pk)
    else:
        form = CollectibleForm(instance=collectible)
    return render(
        request,
        "collectibles/collectible_form.html",
        {
            "form": form,
            "title": "Update Collectible",
            "images": images,
        },
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

            model = llm.get_model("gpt-4.1-nano")

            # Use the primary image for AI enhancement if available
            primary_image = collectible.images.filter(is_primary=True).first()
            attachment_path = primary_image.image.path if primary_image else None
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
                attachments=[llm.Attachment(path=attachment_path)]
                if attachment_path
                else [],
                key=OPENAI_API_KEY,
            ).json()

            # Example response structure from the LLM service
            # {
            #     'content': (
            #         '{"name":"Vintage Fujifilm X-T10 Mirrorless Camera with 18-55mm Lens",'
            #         '"description":"C...lens, ready for your creative endeavors."}'
            #     ),
            #     'finish_reason': 'stop',
            #     'usage': {
            #         'completion_tokens': 125,
            #         'prompt_tokens': 3823,
            #         'total_tokens': 3948,
            #         'completion_tokens_details': {...},
            #         'prompt_tokens_details': {...}
            #     },
            #     'id': 'chatcmpl-BkEJxCVOi9xLfRsxZUqq7Vs85xmAR',
            #     'object': 'chat.completion.chunk',
            #     'model': 'gpt-4.1-nano-2025-04-14',
            #     'created': 1750357837
            # }

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
