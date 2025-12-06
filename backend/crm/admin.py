from django.contrib import admin
from .models import Contact, Deal, Interaction, NextAction


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['contact_name', 'company', 'email', 'status', 'priority', 'date_added']
    list_filter = ['status', 'priority', 'source']
    search_fields = ['contact_name', 'company', 'email']


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ['contact', 'deal_stage', 'deal_value_usd', 'probability_pct', 'expected_close_date']
    list_filter = ['deal_stage', 'status_flags']
    search_fields = ['contact__contact_name', 'contact__company', 'service']


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ['contact', 'interaction_type', 'direction', 'interaction_date']
    list_filter = ['interaction_type', 'direction']
    search_fields = ['contact__contact_name', 'notes']


@admin.register(NextAction)
class NextActionAdmin(admin.ModelAdmin):
    list_display = ['contact', 'action', 'due_date', 'priority', 'status']
    list_filter = ['status', 'priority', 'due_date']
    search_fields = ['action', 'contact__contact_name']

