from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import uuid
from .models import Contact, Deal, Interaction
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
    """List all deals"""
    user_id = request.user.id
    deals = Deal.objects.select_related('contact').filter(user_id=user_id)
    return render(request, 'crm/deal_list.html', {'deals': deals})


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
    """CRM Dashboard with revenue metrics"""
    from django.utils import timezone
    from datetime import timedelta, date
    from decimal import Decimal
    
    user_id = request.user.id
    now = timezone.now()
    today = date.today()
    this_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_week = now + timedelta(days=7)
    
    # Get all deals
    all_deals = Deal.objects.select_related('contact').filter(user_id=user_id)
    
    # Revenue this month (closed won deals closed this month)
    this_month_start_date = this_month_start.date() if hasattr(this_month_start, 'date') else date(this_month_start.year, this_month_start.month, 1)
    next_month_start_date = date(this_month_start_date.year, this_month_start_date.month + 1, 1) if this_month_start_date.month < 12 else date(this_month_start_date.year + 1, 1, 1)
    
    closed_won_this_month = all_deals.filter(
        deal_stage='Closed Won',
        expected_close_date__gte=this_month_start_date,
        expected_close_date__lt=next_month_start_date
    )
    revenue_mtd = sum(deal.deal_value_usd or Decimal('0') for deal in closed_won_this_month)
    
    # Weighted pipeline (deal_value * probability)
    weighted_pipeline = sum(
        (deal.deal_value_usd or Decimal('0')) * Decimal(deal.probability_pct) / 100
        for deal in all_deals.exclude(deal_stage__in=['Closed Won', 'Closed Lost'])
    )
    
    # Deals closing this week
    deals_closing_this_week = all_deals.filter(
        expected_close_date__gte=today,
        expected_close_date__lte=next_week.date()
    ).exclude(deal_stage__in=['Closed Won', 'Closed Lost']).count()
    
    # Average deal size
    deals_with_value = all_deals.exclude(deal_value_usd__isnull=True).exclude(deal_value_usd=0)
    avg_deal_size = sum(deal.deal_value_usd for deal in deals_with_value) / len(deals_with_value) if deals_with_value else Decimal('0')
    
    # All deals for table (exclude closed lost)
    active_deals = all_deals.exclude(deal_stage='Closed Lost').order_by('-expected_close_date', '-created_at')
    
    context = {
        'revenue_mtd': revenue_mtd,
        'weighted_pipeline': weighted_pipeline,
        'deals_closing_this_week': deals_closing_this_week,
        'avg_deal_size': avg_deal_size,
        'deals': active_deals,
        'today': today,
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

