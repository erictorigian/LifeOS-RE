from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import uuid
from .models import Contact, Deal, Interaction, NextAction
from .forms import ContactForm, DealForm, InteractionForm


@login_required
def contact_list(request):
    """List all contacts"""
    user_id = request.user.id
    contacts = Contact.objects.filter(user_id=user_id)
    return render(request, 'crm/contact_list.html', {'contacts': contacts})


@login_required
def contact_create(request):
    """Create a new contact"""
    user_id = request.user.id
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user_id = user_id
            contact.save()
            messages.success(request, 'Contact created successfully!')
            return redirect('crm:contact_list')
    else:
        form = ContactForm()
    return render(request, 'crm/contact_form.html', {'form': form, 'title': 'Create Contact'})


@login_required
def contact_update(request, pk):
    """Update an existing contact"""
    user_id = request.user.id
    contact = get_object_or_404(Contact, pk=pk, user_id=user_id)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user_id = user_id
            contact.save()
            messages.success(request, 'Contact updated successfully!')
            return redirect('crm:contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'crm/contact_form.html', {'form': form, 'contact': contact, 'title': 'Update Contact'})


@login_required
def contact_delete(request, pk):
    """Delete a contact"""
    user_id = request.user.id
    contact = get_object_or_404(Contact, pk=pk, user_id=user_id)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, 'Contact deleted successfully!')
        return redirect('crm:contact_list')
    return render(request, 'crm/contact_confirm_delete.html', {'contact': contact})


@login_required
def deal_list(request):
    """List all deals, separated by monthly/recurring and one-time"""
    user_id = request.user.id
    all_deals = Deal.objects.select_related('contact').filter(user_id=user_id).order_by('-expected_close_date', '-created_at')
    
    # Separate deals by billing frequency
    monthly_deals = all_deals.filter(billing_frequency__in=['Monthly', 'Quarterly', 'Annually'])
    one_time_deals = all_deals.filter(billing_frequency='One-time')
    other_deals = all_deals.exclude(billing_frequency__in=['Monthly', 'Quarterly', 'Annually', 'One-time'])
    
    return render(request, 'crm/deal_list.html', {
        'monthly_deals': monthly_deals,
        'one_time_deals': one_time_deals,
        'other_deals': other_deals,
        'all_deals': all_deals,  # For backwards compatibility
    })


@login_required
def deal_create(request):
    """Create a new deal"""
    user_id = request.user.id
    if request.method == 'POST':
        form = DealForm(request.POST)
        if form.is_valid():
            deal = form.save(commit=False)
            deal.user_id = user_id
            deal.save()
            messages.success(request, 'Deal created successfully!')
            return redirect('crm:deal_list')
    else:
        form = DealForm()
        # Filter contacts to only show this user's contacts
        form.fields['contact'].queryset = Contact.objects.filter(user_id=user_id)
    return render(request, 'crm/deal_form.html', {'form': form, 'title': 'Create Deal'})


@login_required
def deal_update(request, pk):
    """Update an existing deal"""
    user_id = request.user.id
    deal = get_object_or_404(Deal, pk=pk, user_id=user_id)
    if request.method == 'POST':
        form = DealForm(request.POST, instance=deal)
        if form.is_valid():
            deal = form.save(commit=False)
            deal.user_id = user_id
            deal.save()
            messages.success(request, 'Deal updated successfully!')
            return redirect('crm:deal_list')
    else:
        form = DealForm(instance=deal)
        # Filter contacts to only show this user's contacts
        form.fields['contact'].queryset = Contact.objects.filter(user_id=user_id)
    return render(request, 'crm/deal_form.html', {'form': form, 'deal': deal, 'title': 'Update Deal'})


@login_required
def deal_delete(request, pk):
    """Delete a deal"""
    user_id = request.user.id
    deal = get_object_or_404(Deal, pk=pk, user_id=user_id)
    if request.method == 'POST':
        deal.delete()
        messages.success(request, 'Deal deleted successfully!')
        return redirect('crm:deal_list')
    return render(request, 'crm/deal_confirm_delete.html', {'deal': deal})


@login_required
def interaction_list(request):
    """List all interactions"""
    user_id = request.user.id
    interactions = Interaction.objects.select_related('contact').filter(user_id=user_id)
    return render(request, 'crm/interaction_list.html', {'interactions': interactions})


@login_required
def interaction_create(request):
    """Create a new interaction"""
    user_id = request.user.id
    if request.method == 'POST':
        form = InteractionForm(request.POST)
        if form.is_valid():
            interaction = form.save(commit=False)
            interaction.user_id = user_id
            interaction.save()
            messages.success(request, 'Interaction created successfully!')
            return redirect('crm:interaction_list')
    else:
        form = InteractionForm()
        # Filter contacts to only show this user's contacts
        form.fields['contact'].queryset = Contact.objects.filter(user_id=user_id)
    return render(request, 'crm/interaction_form.html', {'form': form, 'title': 'Create Interaction'})


@login_required
def interaction_update(request, pk):
    """Update an existing interaction"""
    user_id = request.user.id
    interaction = get_object_or_404(Interaction, pk=pk, user_id=user_id)
    if request.method == 'POST':
        form = InteractionForm(request.POST, instance=interaction)
        if form.is_valid():
            interaction = form.save(commit=False)
            interaction.user_id = user_id
            interaction.save()
            messages.success(request, 'Interaction updated successfully!')
            return redirect('crm:interaction_list')
    else:
        form = InteractionForm(instance=interaction)
        # Filter contacts to only show this user's contacts
        form.fields['contact'].queryset = Contact.objects.filter(user_id=user_id)
    return render(request, 'crm/interaction_form.html', {'form': form, 'interaction': interaction, 'title': 'Update Interaction'})


@login_required
def interaction_delete(request, pk):
    """Delete an interaction"""
    user_id = request.user.id
    interaction = get_object_or_404(Interaction, pk=pk, user_id=user_id)
    if request.method == 'POST':
        interaction.delete()
        messages.success(request, 'Interaction deleted successfully!')
        return redirect('crm:interaction_list')
    return render(request, 'crm/interaction_confirm_delete.html', {'interaction': interaction})


@login_required
def dashboard(request):
    """CRM Dashboard focused on deals, customers, and next steps"""
    from django.utils import timezone
    from datetime import timedelta, date
    from decimal import Decimal
    from collections import defaultdict
    
    user_id = request.user.id
    now = timezone.now()
    today = date.today()
    next_week = today + timedelta(days=7)
    next_month = today + timedelta(days=30)
    
    # Get all deals with contacts
    all_deals = Deal.objects.select_related('contact').filter(user_id=user_id)
    active_deals = all_deals.exclude(deal_stage__in=['Closed Won', 'Closed Lost']).order_by('-expected_close_date', '-created_at')
    
    # Get next actions from NextAction model
    upcoming_actions = NextAction.objects.select_related('contact', 'deal').filter(
        user_id=user_id,
        status='Pending',
        due_date__gte=today
    ).order_by('due_date')[:10]
    
    # Get next steps from deals (next_action field)
    deal_next_steps = []
    for deal in active_deals:
        if deal.next_action and deal.next_action_due:
            deal_next_steps.append({
                'deal': deal,
                'action': deal.next_action,
                'due_date': deal.next_action_due,
                'contact': deal.contact,
            })
    
    # Sort and combine next steps
    all_next_steps = sorted(
        deal_next_steps,
        key=lambda x: x['due_date']
    )[:10]
    
    # Separate monthly/recurring deals from one-time deals (from ALL deals, not just active)
    monthly_deals_all = all_deals.filter(billing_frequency__in=['Monthly', 'Quarterly', 'Annually'])
    one_time_deals_all = all_deals.filter(billing_frequency='One-time')
    # Deals without billing_frequency - we'll include their values in totals but show separately
    no_frequency_deals_all = all_deals.exclude(billing_frequency__in=['Monthly', 'Quarterly', 'Annually', 'One-time'])
    
    # For display, use active deals only
    monthly_deals = active_deals.filter(billing_frequency__in=['Monthly', 'Quarterly', 'Annually'])
    one_time_deals = active_deals.filter(billing_frequency='One-time')
    no_frequency_deals = active_deals.exclude(billing_frequency__in=['Monthly', 'Quarterly', 'Annually', 'One-time'])
    
    # Group monthly deals by contact
    monthly_deals_by_contact = defaultdict(list)
    for deal in monthly_deals:
        monthly_deals_by_contact[deal.contact].append(deal)
    
    # Group one-time deals by contact
    one_time_deals_by_contact = defaultdict(list)
    for deal in one_time_deals:
        one_time_deals_by_contact[deal.contact].append(deal)
    
    # Group deals without frequency by contact (for backwards compatibility)
    no_frequency_deals_by_contact = defaultdict(list)
    for deal in no_frequency_deals:
        no_frequency_deals_by_contact[deal.contact].append(deal)
    
    # Calculate key metrics - use ALL deals for total values (including closed)
    total_pipeline = sum(deal.deal_value_usd or Decimal('0') for deal in active_deals)
    weighted_pipeline = sum(
        (deal.deal_value_usd or Decimal('0')) * Decimal(deal.probability_pct) / 100
        for deal in active_deals
    )
    
    # Monthly/Recurring total value (sum of all recurring deal values from ALL deals)
    monthly_total_value = sum(deal.deal_value_usd or Decimal('0') for deal in monthly_deals_all)
    
    # One-time total value (sum of all one-time deal values from ALL deals)
    one_time_total_value = sum(deal.deal_value_usd or Decimal('0') for deal in one_time_deals_all)
    
    # Debug: Check if deals exist and have values
    # If deals don't have billing_frequency set, they won't be in monthly or one-time
    # Let's also check deals without frequency
    no_freq_total = sum(deal.deal_value_usd or Decimal('0') for deal in no_frequency_deals_all)
    
    # If there are deals without billing_frequency, we could add them to totals
    # For now, let's make sure we're at least seeing all deals with values
    
    # Monthly recurring revenue (MRR) - sum of monthly deals
    mrr = sum(deal.deal_value_usd or Decimal('0') for deal in monthly_deals.filter(billing_frequency='Monthly'))
    # Add quarterly/annual converted to monthly
    for deal in monthly_deals:
        if deal.billing_frequency == 'Quarterly' and deal.deal_value_usd:
            mrr += (deal.deal_value_usd or Decimal('0')) / 3
        elif deal.billing_frequency == 'Annually' and deal.deal_value_usd:
            mrr += (deal.deal_value_usd or Decimal('0')) / 12
    
    # Deals closing soon
    deals_closing_soon = active_deals.filter(
        expected_close_date__gte=today,
        expected_close_date__lte=next_month
    )
    
    # Debug info - check all deals
    all_deals_count = all_deals.count()
    all_deals_with_value = [d for d in all_deals if d.deal_value_usd]
    all_deals_with_freq = [d for d in all_deals if d.billing_frequency]
    
    context = {
        'monthly_deals_by_contact': dict(monthly_deals_by_contact),
        'one_time_deals_by_contact': dict(one_time_deals_by_contact),
        'no_frequency_deals_by_contact': dict(no_frequency_deals_by_contact),
        'next_steps': all_next_steps,
        'upcoming_actions': upcoming_actions,
        'total_pipeline': total_pipeline,
        'weighted_pipeline': weighted_pipeline,
        'monthly_total_value': monthly_total_value,
        'one_time_total_value': one_time_total_value,
        'no_freq_total': no_freq_total,  # For debugging
        'mrr': mrr,
        'deals_closing_soon': deals_closing_soon,
        'active_deals_count': active_deals.count(),
        'monthly_deals_count': monthly_deals.count(),
        'one_time_deals_count': one_time_deals.count(),
        'all_deals_count': all_deals_count,  # Debug
        'all_deals_with_value_count': len(all_deals_with_value),  # Debug
        'all_deals_with_freq_count': len(all_deals_with_freq),  # Debug
        'today': today,
        'next_week': next_week,
    }
    return render(request, 'crm/dashboard.html', context)


@login_required
def deal_detail_json(request, pk):
    """Return deal details as JSON for slide-over"""
    from django.http import JsonResponse
    from django.utils.dateformat import format
    
    user_id = request.user.id
    deal = get_object_or_404(Deal, pk=pk, user_id=user_id)
    
    return JsonResponse({
        'company': deal.contact.company,
        'contact_name': deal.contact.contact_name,
        'deal_value': f"${deal.deal_value_usd:,.0f}" if deal.deal_value_usd else None,
        'stage': deal.deal_stage,
        'probability': deal.probability_pct,
        'expected_close': deal.expected_close_date.strftime('%B %d, %Y') if deal.expected_close_date else None,
        'next_action': deal.next_action,
        'next_action_due': deal.next_action_due.strftime('%B %d, %Y') if deal.next_action_due else None,
        'notes': deal.notes,
        'service': deal.service,
        'engagement': deal.engagement,
    })

