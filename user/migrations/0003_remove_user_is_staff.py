# Generated by Django 5.0.3 on 2024-03-25 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_user_is_staff"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="is_staff",
        ),
    ]
