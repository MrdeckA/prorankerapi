# Generated by Django 5.0.3 on 2024-03-31 02:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("candidat", "0007_alter_candidat_telephone"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="candidat",
            name="adresse",
        ),
        migrations.RemoveField(
            model_name="candidat",
            name="cv_original_name",
        ),
        migrations.RemoveField(
            model_name="candidat",
            name="prenom",
        ),
    ]