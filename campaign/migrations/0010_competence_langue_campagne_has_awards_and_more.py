# Generated by Django 5.0.2 on 2024-02-17 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("campaign", "0009_collaborateur_critere"),
    ]

    operations = [
        migrations.CreateModel(
            name="Competence",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Langue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name="campagne",
            name="has_awards",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="campagne",
            name="has_certifications",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="campagne",
            name="minimum_degree",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="campagne",
            name="minimum_number_of_experiences",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="campagne",
            name="minimum_number_of_languages",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="campagne",
            name="minimum_number_of_years_of_experience",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="campagne",
            name="skills",
            field=models.ManyToManyField(to="campaign.competence"),
        ),
        migrations.AddField(
            model_name="campagne",
            name="languages",
            field=models.ManyToManyField(to="campaign.langue"),
        ),
        migrations.DeleteModel(
            name="Critere",
        ),
    ]
