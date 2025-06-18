from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Collectible
from collectibles.forms import CollectibleForm

# List all collectibles
def collectible_list(request):
    collectibles = Collectible.objects.filter(is_sold=False).order_by('-created_at')
    return render(request, 'collectibles/collectible_list.html', {'collectibles': collectibles})

# View a single collectible
def collectible_detail(request, pk):
    collectible = get_object_or_404(Collectible, pk=pk)
    return render(request, 'collectibles/collectible_detail.html', {'collectible': collectible})

# Create a new collectible
@login_required
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
    collectible = get_object_or_404(Collectible, pk=pk, owner=request.user) # Ensure only owner can update
    if request.method == 'POST':
        form = CollectibleForm(request.POST, request.FILES, instance=collectible)
        if form.is_valid():
            form.save()
            messages.success(request, 'Collectible updated successfully!')
            return redirect('collectible_detail', pk=collectible.pk)
    else:
        form = CollectibleForm(instance=collectible)
    return render(request, 'collectibles/collectible_form.html', {'form': form, 'title': 'Update Collectible'})

# Delete a collectible
# @login_required
def collectible_delete(request, pk):
    collectible = get_object_or_404(Collectible, pk=pk, owner=request.user) # Ensure only owner can delete
    if request.method == 'POST':
        collectible.delete()
        messages.success(request, 'Collectible deleted successfully!')
        return redirect('collectible_list')
    return render(request, 'collectibles/collectible_confirm_delete.html', {'collectible': collectible})