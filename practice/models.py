import uuid

from django.db import models
from django.db.models import Q

IN_PROGRESS = "in_progress"
COMPLETED = "completed"


class PracticeAttempt(models.Model):
    """One practice set. `questions` is a JSON snapshot (incl. answers, server-side only)."""

    STATUS_CHOICES = [(IN_PROGRESS, "In progress"), (COMPLETED, "Completed")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.CharField(max_length=20)
    difficulty = models.CharField(max_length=10)
    questions = models.JSONField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=IN_PROGRESS)
    total_questions = models.PositiveIntegerField()
    answered_count = models.PositiveIntegerField(default=0)
    correct_count = models.PositiveIntegerField(default=0)
    percentage = models.FloatField(null=True, blank=True)
    details = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=Q(percentage__isnull=True)
                | (Q(percentage__gte=0) & Q(percentage__lte=100)),
                name="percentage_between_0_and_100",
            )
        ]

    def __str__(self):
        return f"{self.topic}/{self.difficulty} [{self.status}] {self.id}"
