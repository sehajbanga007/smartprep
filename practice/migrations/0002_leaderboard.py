from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("practice", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="practiceattempt",
            name="player_name",
            field=models.CharField(default="Anonymous", max_length=20),
        ),
        migrations.AddField(
            model_name="practiceattempt",
            name="time_taken_seconds",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddIndex(
            model_name="practiceattempt",
            index=models.Index(fields=["status", "topic", "difficulty"], name="leaderboard_lookup"),
        ),
    ]
