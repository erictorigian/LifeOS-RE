from django.db import models
from django.utils import timezone
import uuid


class Vision(models.Model):
    """
    A big-picture destination / identity / reality definition.
    Example: 'LifeOS Franchise', '$100K/mo Revenue Engine', 'World-Class Father'.
    """
    id = models.BigAutoField(primary_key=True)

    # Who owns this vision (Supabase auth user ID, not a Django FK for now)
    user_id = models.UUIDField()

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # JSON ruleset: identity statements, rules, constraints, mantras, etc.
    ruleset = models.JSONField(default=dict, blank=True)

    # Optional: category or tag, e.g. 'business', 'health', 'family'
    category = models.CharField(max_length=100, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} (user {self.user_id})"


class Timeline(models.Model):
    """
    A specific stream of blocks under a Vision.
    Example: 'Franchise – MVP Dev', 'Revenue – Sales Execution', 'CRM – Follow-ups'.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    vision = models.ForeignKey(
        Vision,
        on_delete=models.CASCADE,
        related_name='timelines'
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    # Optional: metadata for advanced use (priority, tags, etc.)
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.name} [{self.vision.title}]"