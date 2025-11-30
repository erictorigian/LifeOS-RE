from django.db import models
from django.utils import timezone
import hashlib
import json
import uuid


class Block(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.UUIDField()

    # New: explicit FKs instead of loose IDs
    vision = models.ForeignKey(
        'visions.Vision',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='blocks'
    )

    timeline = models.ForeignKey(
        'visions.Timeline',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='blocks'
    )

    # main content (your 3–5 second moment)
    content = models.JSONField()

    created_at = models.DateTimeField(default=timezone.now)

    prev_block = models.ForeignKey(
        "self", null=True, blank=True, related_name="next_blocks", on_delete=models.SET_NULL
    )
    next_block = models.ForeignKey(
        "self", null=True, blank=True, related_name="prev_blocks", on_delete=models.SET_NULL
    )

    hash = models.TextField(null=True, blank=True)
    prev_hash = models.TextField(null=True, blank=True)

    # timeline_id column is now represented by the FK 'timeline'
    # if you want a branch ID separate from Timeline, we can reintroduce later
    # for now, Timeline IS the branch identifier.
    # timeline_id = models.UUIDField(default=uuid.uuid4)  # <-- remove this line

    def compute_hash(self):
        block_string = json.dumps({
            "id": self.id,
            "user_id": str(self.user_id),
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "prev_hash": self.prev_hash or "",
        }, sort_keys=True)

        return hashlib.sha256(block_string.encode()).hexdigest()

    def save(self, *args, **kwargs):
        if self.prev_block:
            self.prev_hash = self.prev_block.hash

        new_hash = self.compute_hash()
        self.hash = new_hash

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Block {self.id} (user {self.user_id})"