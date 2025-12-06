from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import uuid
from .models import Contact, Deal, Interaction
from .forms import ContactForm, DealForm, InteractionForm

# User ID to use for CRM data
USER_ID = uuid.UUID('11111111-1111-1111-1111-111111111111')


def contact_list(request):
    """List all contacts"""
    contacts = Contact.objects.filter(user_id=USER_ID)
    return render(request, 'crm/contact_list.html', {'contacts': contacts})


def contact_create(request):
    """Create a new contact"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user_id = USER_ID
            contact.save()
            messages.success(request, 'Contact created successfully!')
            return redirect('crm:contact_list')
    else:
        form = ContactForm()
    return render(request, 'crm/contact_form.html', {'form': form, 'title': 'Create Contact'})


def contact_update(request, pk):
    """Update an existing contact"""
    contact = get_object_or_404(Contact, pk=pk, user_id=USER_ID)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user_id = USER_ID
            contact.save()
            messages.success(request, 'Contact updated successfully!')
            return redirect('crm:contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'crm/contact_form.html', {'form': form, 'contact': contact, 'title': 'Update Contact'})


def contact_delete(request, pk):
    """Delete a contact"""
    contact = get_object_or_404(Contact, pk=pk, user_id=USER_ID)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, 'Contact deleted successfully!')
        return redirect('crm:contact_list')
    return render(request, 'crm/contact_confirm_delete.html', {'contact': contact})


def deal_list(request):
    """List all deals"""
    deals = Deal.objects.select_related('contact').filter(user_id=USER_ID)
    return render(request, 'crm/deal_list.html', {'deals': deals})


def deal_create(request):
    """Create a new deal"""
    if request.method == 'POST':
        form = DealForm(request.POST)
        if form.is_valid():
            deal = form.save(commit=False)
            deal.user_id = USER_ID
            deal.save()
            messages.success(request, 'Deal created successfully!')
            return redirect('crm:deal_list')
    else:
        form = DealForm()
        # Filter contacts to only show this user's contacts
        form.fields['contact'].queryset = Contact.objects.filter(user_id=USER_ID)
    return render(request, 'crm/deal_form.html', {'form': form, 'title': 'Create Deal'})


def deal_update(request, pk):
    """Update an existing deal"""
    deal = get_object_or_404(Deal, pk=pk, user_id=USER_ID)
    if request.method == 'POST':
        form = DealForm(request.POST, instance=deal)
        if form.is_valid():
            deal = form.save(commit=False)
            deal.user_id = USER_ID
            deal.save()
            messages.success(request, 'Deal updated successfully!')
            return redirect('crm:deal_list')
    else:
        form = DealForm(instance=deal)
        # Filter contacts to only show this user's contacts
        form.fields['contact'].queryset = Contact.objects.filter(user_id=USER_ID)
    return render(request, 'crm/deal_form.html', {'form': form, 'deal': deal, 'title': 'Update Deal'})


def deal_delete(request, pk):
    """Delete a deal"""
    deal = get_object_or_404(Deal, pk=pk, user_id=USER_ID)
    if request.method == 'POST':
        deal.delete()
        messages.success(request, 'Deal deleted successfully!')
        return redirect('crm:deal_list')
    return render(request, 'crm/deal_confirm_delete.html', {'deal': deal})


def interaction_list(request):
    """List all interactions"""
    interactions = Interaction.objects.select_related('contact').filter(user_id=USER_ID)
    return render(request, 'crm/interaction_list.html', {'interactions': interactions})


def interaction_create(request):
    """Create a new interaction"""
    if request.method == 'POST':
        form = InteractionForm(request.POST)
        if form.is_valid():
            interaction = form.save(commit=False)
            interaction.user_id = USER_ID
            interaction.save()
            messages.success(request, 'Interaction created successfully!')
            return redirect('crm:interaction_list')
    else:
        form = InteractionForm()
        # Filter contacts to only show this user's contacts
        form.fields['contact'].queryset = Contact.objects.filter(user_id=USER_ID)
    return render(request, 'crm/interaction_form.html', {'form': form, 'title': 'Create Interaction'})


def interaction_update(request, pk):
    """Update an existing interaction"""
    interaction = get_object_or_404(Interaction, pk=pk, user_id=USER_ID)
    if request.method == 'POST':
        form = InteractionForm(request.POST, instance=interaction)
        if form.is_valid():
            interaction = form.save(commit=False)
            interaction.user_id = USER_ID
            interaction.save()
            messages.success(request, 'Interaction updated successfully!')
            return redirect('crm:interaction_list')
    else:
        form = InteractionForm(instance=interaction)
        # Filter contacts to only show this user's contacts
        form.fields['contact'].queryset = Contact.objects.filter(user_id=USER_ID)
    return render(request, 'crm/interaction_form.html', {'form': form, 'interaction': interaction, 'title': 'Update Interaction'})


def interaction_delete(request, pk):
    """Delete an interaction"""
    interaction = get_object_or_404(Interaction, pk=pk, user_id=USER_ID)
    if request.method == 'POST':
        interaction.delete()
        messages.success(request, 'Interaction deleted successfully!')
        return redirect('crm:interaction_list')
    return render(request, 'crm/interaction_confirm_delete.html', {'interaction': interaction})


def dashboard(request):
    """CRM Dashboard"""
    contacts_count = Contact.objects.filter(user_id=USER_ID).count()
    deals_count = Deal.objects.filter(user_id=USER_ID).count()
    interactions_count = Interaction.objects.filter(user_id=USER_ID).count()
    
    recent_contacts = Contact.objects.filter(user_id=USER_ID)[:5]
    recent_deals = Deal.objects.select_related('contact').filter(user_id=USER_ID)[:5]
    recent_interactions = Interaction.objects.select_related('contact').filter(user_id=USER_ID)[:5]
    
    context = {
        'contacts_count': contacts_count,
        'deals_count': deals_count,
        'interactions_count': interactions_count,
        'recent_contacts': recent_contacts,
        'recent_deals': recent_deals,
        'recent_interactions': recent_interactions,
    }
    return render(request, 'crm/dashboard.html', context)

