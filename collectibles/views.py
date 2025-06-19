import json

import llm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.utils.datastructures import MultiValueDict

from collectibles.forms import CollectibleForm

from .models import Collectible


# List all collectibles
def collectible_list(request):
    collectibles = Collectible.objects.filter(
        is_sold=False).order_by('-created_at')
    return render(request, 'collectibles/collectible_list.html', {'collectibles': collectibles})

# View a single collectible


def collectible_detail(request, pk):
    collectible = get_object_or_404(Collectible, pk=pk)
    return render(request, 'collectibles/collectible_detail.html', {'collectible': collectible})

# Create a new collectible


# @login_required
def collectible_create(request):
    if request.method == 'POST':
        form = CollectibleForm(request.POST, request.FILES)
        if form.is_valid():
            collectible = form.save(commit=False)
            collectible.owner = request.user
            collectible.save()
            messages.success(request, 'Collectible added successfully!')
            return redirect('collectible_detail', pk=collectible.pk)
    else:
        form = CollectibleForm()
    return render(request, 'collectibles/collectible_form.html', {'form': form, 'title': 'List New Collectible'})

# Update an existing collectible
# @login_required


def collectible_update(request, pk):
    # Ensure only owner can update
    collectible = get_object_or_404(Collectible, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = CollectibleForm(
            request.POST, request.FILES, instance=collectible)
        if form.is_valid():
            form.save()
            messages.success(request, 'Collectible updated successfully!')
            return redirect('collectible_detail', pk=collectible.pk)
    else:
        form = CollectibleForm(instance=collectible)
    return render(request, 'collectibles/collectible_form.html', {'form': form, 'title': 'Update Collectible'})

# @login_required
def collectible_delete(request, pk):
    # Ensure only owner can delete
    collectible = get_object_or_404(Collectible, pk=pk, owner=request.user)
    if request.method == 'POST':
        collectible.delete()
        messages.success(request, 'Collectible deleted successfully!')
        return redirect('collectible_list')
    return render(request, 'collectibles/collectible_confirm_delete.html', {'collectible': collectible})


# @login_required
def enhance_with_ai(request, pk):
    # Ensure only owner can enhance
    collectible = get_object_or_404(Collectible, pk=pk, owner=request.user)
    
    # Mock AI enhancement (similar to improve_collectible_description_ai)
    try:
        # Create a mock response or call the LLM service
        mock_response = True  # Set to False to use actual LLM

        if mock_response:
            # Mock improved response
            enhanced = {
                "name": "Mock AI Enhanced Name",
                "description": ("Mocka AI Enhanced Description."),
            }
        else:
            # Here you would call the LLM service with a prompt
            prompt = f"""
            You are an expert e-commerce copywriter and market analyst specializing in collectible items.
            Your task is to improve a collectible listing's name and description for an eBay-like marketplace.
            You should also suggest a competitive and appealing price for the item.

            Focus on making the description more engaging, detailed, professional, and appealing to potential buyers.
            Highlight key features and benefits, and use clear, concise language.
            Consider the item's current details and condition when suggesting the price.
            The suggested price should be a reasonable numerical value, suitable for an online marketplace.

            Current Collectible Details:
            Name: {collectible.name}
            Description: {collectible.description}
            Current Price: ${collectible.price}
            Condition: {collectible.condition}

            Please return the improved name, description, and a suggested price in JSON format with the keys 'name', 'description', and 'price'. The price should be a number (float or integer).
            Example format:
            {{
                "name": "Improved Name Here",
                "description": "Improved, detailed description here.",
                "price": 99.99
            }}
            """
            try:
                model = llm.get_model("gpt-3.5-turbo")  # Example model
            except Exception as e:
                print(f"Warning: Could not get specified LLM model. Falling back to default: {e}")
                model = llm.get_default_model()

            llm_response = model.prompt(prompt) # type: ignore
            llm_output_text = llm_response.text().strip() # type: ignore

            if llm_output_text.startswith("```json") and llm_output_text.endswith("```"):
                llm_output_text = llm_output_text[7:-3].strip()
                
            enhanced = json.loads(llm_output_text)
        
        # Pass the original and enhanced data to the template
        original = {
            "name": collectible.name,
            "description": collectible.description,
        }
        
        return render(request, 'collectibles/collectible_enhanced.html', {
            'collectible': collectible,
            'original': original,
            'enhanced': enhanced
        })
        
    except Exception as e:
        print(f"AI Enhancement Error: {e}")
        messages.error(request, f"An error occurred during AI enhancement: {str(e)}")
        return redirect('collectible_detail', pk=pk)


# @login_required
@require_POST
def save_enhanced(request, pk):
    # Ensure only owner can save enhanced version
    collectible = get_object_or_404(Collectible, pk=pk, owner=request.user)
    
    try:
        # Get the enhanced data from the form
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        # Update the collectible
        collectible.name = name
        collectible.description = description
        collectible.save()
        
        messages.success(request, 'Enhanced collectible saved successfully!')
        return redirect('collectible_detail', pk=pk)
        
    except Exception as e:
        print(f"Save Enhanced Error: {e}")
        messages.error(request, f"An error occurred while saving the enhanced collectible: {str(e)}")
        return redirect('collectible_detail', pk=pk)
