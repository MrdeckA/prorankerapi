from django.db import models
import sys
import fitz

from django.contrib.auth.models import User


class Campagne(models.Model):
    nom = models.CharField(max_length=255, blank=False, default="")
    description = models.TextField(default="", blank=False)
    intitule_poste = models.CharField(max_length=255, blank=False, default="")
    minimum_number_of_languages = models.IntegerField(default=0)
    minimum_number_of_experiences = models.IntegerField(default=0)
    minimum_number_of_years_of_experience = models.IntegerField(default=0)
    minimum_degree = models.CharField(max_length=255, default="")
    languages = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    has_awards = models.BooleanField(default=False)
    has_certifications = models.BooleanField(default=False)

    def __str__(self):
        return self.nom


class Candidat(models.Model):
    campagne = models.ForeignKey(
        Campagne, on_delete=models.CASCADE, related_name='candidats')
    nom = models.CharField(max_length=255, blank=True)
    prenom = models.CharField(max_length=255, blank=True)
    cv_path = models.TextField(blank=True)
    adresse = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    telephone = models.CharField(max_length=15, blank=True)
    cv_data_url = models.TextField(blank=False)  # Champs requis
    cv_original_name = models.TextField(
        blank=False)  # Champs requis

    def __str__(self):
        return f'{self.prenom} {self.nom} - Campagne: {self.campagne.nom}'


class Collaborateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    campagne = models.ForeignKey(
        Campagne, on_delete=models.CASCADE, related_name='collaborateurs')

    def __str__(self):
        return f'Collaborateur: {self.user.username} - Campagne: {self.campagne.nom}'
