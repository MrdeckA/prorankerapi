# Generated by Django 5.0.3 on 2024-06-21 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("campagne", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="campagne",
            name="files",
            field=models.JSONField(blank=True, default=None),
        ),
    ]
