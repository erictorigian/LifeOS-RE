from django.db import models
from django.utils import timezone
import uuid


class Contact(models.Model):
    """CRM Contact model matching crm_contacts table"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.TextField()
    contact_name = models.TextField()
    role = models.TextField(blank=True, null=True)
    email = models.TextField(unique=True, blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)
    source = models.TextField(blank=True, null=True)
    priority = models.TextField(default='Med')
    status = models.TextField(default='Active')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'crm_contacts'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.contact_name} - {self.company}"


class Deal(models.Model):
    """CRM Deal model matching crm_deals table"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='deals')
    engagement = models.TextField(blank=True, null=True)
    service = models.TextField(blank=True, null=True)
    deal_stage = models.TextField()
    probability_pct = models.IntegerField(default=0)
    expected_close_date = models.DateField(blank=True, null=True)
    deal_value_usd = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    retainer_usd = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    billing_frequency = models.TextField(blank=True, null=True)
    next_action = models.TextField(blank=True, null=True)
    next_action_due = models.DateField(blank=True, null=True)
    last_contact_date = models.DateField(blank=True, null=True)
    last_action = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    status_flags = models.JSONField(default=list, blank=True, null=True)
    tags = models.JSONField(default=list, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'crm_deals'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.contact.company} - {self.deal_stage}"


class Interaction(models.Model):
    """CRM Interaction model matching crm_interactions table"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.TextField()
    interaction_date = models.DateTimeField(default=timezone.now)
    direction = models.TextField(choices=[('inbound', 'Inbound'), ('outbound', 'Outbound')], blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    outcome = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'crm_interactions'
        ordering = ['-interaction_date']

    def __str__(self):
        return f"{self.contact.contact_name} - {self.interaction_type}"


class NextAction(models.Model):
    """CRM Next Action model matching crm_next_actions table"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='next_actions')
    deal = models.ForeignKey(Deal, on_delete=models.SET_NULL, blank=True, null=True, related_name='next_actions')
    action = models.TextField()
    due_date = models.DateField()
    priority = models.TextField(default='Med')
    status = models.TextField(default='Pending')
    completed_at = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'crm_next_actions'
        ordering = ['due_date']

    def __str__(self):
        return f"{self.contact.contact_name} - {self.action}"

