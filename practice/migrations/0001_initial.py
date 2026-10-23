import uuid

from django.db import migrations, models
from django.db.models import Q


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PracticeAttempt",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("topic", models.CharField(max_length=20)),
                ("difficulty", models.CharField(max_length=10)),
                ("questions", models.JSONField()),
                ("status", models.CharField(choices=[("in_progress", "In progress"), ("completed", "Completed")], default="in_progress", max_length=12)),
                ("total_questions", models.PositiveIntegerField()),
                ("answered_count", models.PositiveIntegerField(default=0)),
                ("correct_count", models.PositiveIntegerField(default=0)),
                ("percentage", models.FloatField(blank=True, null=True)),
                ("details", models.JSONField(blank=True, default=list)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddConstraint(
            model_name="practiceattempt",
            constraint=models.CheckConstraint(
                condition=Q(percentage__isnull=True) | (Q(percentage__gte=0) & Q(percentage__lte=100)),
                name="percentage_between_0_and_100",
            ),
        ),
    ]
