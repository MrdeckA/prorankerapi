from django.db import models
from campagne.models import Campagne
# Create your models here.
import uuid
class Candidat(models.Model):
    campagne = models.ForeignKey(
        Campagne, on_delete=models.CASCADE, related_name='candidats')
    nom = models.CharField(max_length=255, blank=True)
    prenom = models.CharField(max_length=255, blank=True)
    cv_path = models.CharField(blank=True)
    adresse = models.CharField(blank=True)
    prenom = models.CharField(blank=True)
    telephone = models.CharField(max_length=15, blank=True)
    cv_original_name = models.CharField(
        blank=False)  # Champs requis

    def __str__(self):
        return f'{self.prenom} {self.nom} - Campagne: {self.campagne.nom}'