from django.db import models
import sys
import fitz

from django.contrib.auth.models import User
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from rest_framework import status


class Campagne(models.Model):
    nom = models.CharField(max_length=255, blank=False, default="")
    description_poste = models.TextField(default="", blank=False)
    intitule_poste = models.CharField(max_length=255, blank=False, default="")
    minimum_number_of_languages = models.IntegerField(default=0)
    minimum_number_of_experiences = models.IntegerField(default=0)
    languages = models.TextField(blank=True, null=True)
    degrees = models.TextField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='campagnes', default=None, blank=False)
    files = models.JSONField(blank=False, default=None)

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


class Collaboration(models.Model):
    inviteur = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='collaborations_envoyees')
    invite = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='collaborations_recues')
    # Vous pouvez ajuster la longueur en fonction de vos besoins
    role = models.CharField(max_length=255, default="")

    def __str__(self):
        return f'Collaboration - Inviteur: {self.inviteur.username} - Invite: {self.invite.username} - Rôle: {self.role}'
