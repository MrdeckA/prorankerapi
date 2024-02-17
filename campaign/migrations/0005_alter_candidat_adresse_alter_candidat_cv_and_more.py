# Generated by Django 5.0.2 on 2024-02-10 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("campaign", "0004_candidat_cv_data_url_candidat_cv_original_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="candidat",
            name="adresse",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="candidat",
            name="cv",
            field=models.FileField(blank=True, upload_to="candidat_cv/"),
        ),
        migrations.AlterField(
            model_name="candidat",
            name="cv_data_url",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="candidat",
            name="cv_original_name",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="candidat",
            name="email",
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name="candidat",
            name="nom",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="candidat",
            name="prenom",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="candidat",
            name="telephone",
            field=models.CharField(blank=True, max_length=15),
        ),
    ]