from django.db import models
from django.utils import timezone
import hashlib
import json
import uuid


class Block(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.UUIDField()
    vision_id = models.BigIntegerField(null=True, blank=True)

    # the main content of the block (3–5 second moment)
    content = models.JSONField()

    created_at = models.DateTimeField(default=timezone.now)

    # chain references
    prev_block = models.ForeignKey(
        "self", null=True, blank=True, related_name="next_blocks", on_delete=models.SET_NULL
    )
    next_block = models.ForeignKey(
        "self", null=True, blank=True, related_name="prev_blocks", on_delete=models.SET_NULL
    )

    # cryptographic chain
    hash = models.TextField(null=True, blank=True)
    prev_hash = models.TextField(null=True, blank=True)

    # timeline branch ID
    timeline_id = models.UUIDField(default=uuid.uuid4)

    def compute_hash(self):
        """
        Compute a SHA-256 hash of the content + timestamp + prev_hash.
        """
        block_string = json.dumps({
            "id": self.id,
            "user_id": str(self.user_id),
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "prev_hash": self.prev_hash or "",
        }, sort_keys=True)

        return hashlib.sha256(block_string.encode()).hexdigest()

    def save(self, *args, **kwargs):
        # handle hashing logic
        if self.prev_block:
            self.prev_hash = self.prev_block.hash

        # compute new hash
        new_hash = self.compute_hash()
        self.hash = new_hash

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Block {self.id} (timeline {self.timeline_id})"