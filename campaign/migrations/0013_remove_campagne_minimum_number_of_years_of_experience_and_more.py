# Generated by Django 5.0.2 on 2024-02-22 02:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("campaign", "0012_remove_campagne_description"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="campagne",
            name="minimum_number_of_years_of_experience",
        ),
        migrations.AddField(
            model_name="campagne",
            name="user",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="campagnes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]