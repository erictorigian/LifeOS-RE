from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Contact, Deal, Interaction
from .forms import ContactForm, DealForm, InteractionForm


def contact_list(request):
    """List all contacts"""
    contacts = Contact.objects.all()
    return render(request, 'crm/contact_list.html', {'contacts': contacts})


def contact_create(request):
    """Create a new contact"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact created successfully!')
            return redirect('crm:contact_list')
    else:
        form = ContactForm()
    return render(request, 'crm/contact_form.html', {'form': form, 'title': 'Create Contact'})


def contact_update(request, pk):
    """Update an existing contact"""
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact updated successfully!')
            return redirect('crm:contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'crm/contact_form.html', {'form': form, 'contact': contact, 'title': 'Update Contact'})


def contact_delete(request, pk):
    """Delete a contact"""
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, 'Contact deleted successfully!')
        return redirect('crm:contact_list')
    return render(request, 'crm/contact_confirm_delete.html', {'contact': contact})


def deal_list(request):
    """List all deals"""
    deals = Deal.objects.select_related('contact').all()
    return render(request, 'crm/deal_list.html', {'deals': deals})


def deal_create(request):
    """Create a new deal"""
    if request.method == 'POST':
        form = DealForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Deal created successfully!')
            return redirect('crm:deal_list')
    else:
        form = DealForm()
    return render(request, 'crm/deal_form.html', {'form': form, 'title': 'Create Deal'})


def deal_update(request, pk):
    """Update an existing deal"""
    deal = get_object_or_404(Deal, pk=pk)
    if request.method == 'POST':
        form = DealForm(request.POST, instance=deal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Deal updated successfully!')
            return redirect('crm:deal_list')
    else:
        form = DealForm(instance=deal)
    return render(request, 'crm/deal_form.html', {'form': form, 'deal': deal, 'title': 'Update Deal'})


def deal_delete(request, pk):
    """Delete a deal"""
    deal = get_object_or_404(Deal, pk=pk)
    if request.method == 'POST':
        deal.delete()
        messages.success(request, 'Deal deleted successfully!')
        return redirect('crm:deal_list')
    return render(request, 'crm/deal_confirm_delete.html', {'deal': deal})


def interaction_list(request):
    """List all interactions"""
    interactions = Interaction.objects.select_related('contact').all()
    return render(request, 'crm/interaction_list.html', {'interactions': interactions})


def interaction_create(request):
    """Create a new interaction"""
    if request.method == 'POST':
        form = InteractionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Interaction created successfully!')
            return redirect('crm:interaction_list')
    else:
        form = InteractionForm()
    return render(request, 'crm/interaction_form.html', {'form': form, 'title': 'Create Interaction'})


def interaction_update(request, pk):
    """Update an existing interaction"""
    interaction = get_object_or_404(Interaction, pk=pk)
    if request.method == 'POST':
        form = InteractionForm(request.POST, instance=interaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Interaction updated successfully!')
            return redirect('crm:interaction_list')
    else:
        form = InteractionForm(instance=interaction)
    return render(request, 'crm/interaction_form.html', {'form': form, 'interaction': interaction, 'title': 'Update Interaction'})


def interaction_delete(request, pk):
    """Delete an interaction"""
    interaction = get_object_or_404(Interaction, pk=pk)
    if request.method == 'POST':
        interaction.delete()
        messages.success(request, 'Interaction deleted successfully!')
        return redirect('crm:interaction_list')
    return render(request, 'crm/interaction_confirm_delete.html', {'interaction': interaction})


def dashboard(request):
    """CRM Dashboard"""
    contacts_count = Contact.objects.count()
    deals_count = Deal.objects.count()
    interactions_count = Interaction.objects.count()
    
    recent_contacts = Contact.objects.all()[:5]
    recent_deals = Deal.objects.select_related('contact').all()[:5]
    recent_interactions = Interaction.objects.select_related('contact').all()[:5]
    
    context = {
        'contacts_count': contacts_count,
        'deals_count': deals_count,
        'interactions_count': interactions_count,
        'recent_contacts': recent_contacts,
        'recent_deals': recent_deals,
        'recent_interactions': recent_interactions,
    }
    return render(request, 'crm/dashboard.html', context)

