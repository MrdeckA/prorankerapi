# Generated by Django 5.0.2 on 2024-02-29 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "campaign",
            "0013_remove_campagne_minimum_number_of_years_of_experience_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="campagne",
            name="files",
            field=models.JSONField(blank=True, default=None),
        ),
    ]