from django.db import models
from campagne.models import Campagne
# Create your models here.
import uuid
class Candidat(models.Model):
    campagne = models.ForeignKey(
        Campagne, on_delete=models.CASCADE, related_name='candidats')
    nom_complet = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    fichier = models.CharField(blank=True)
    fichier_sauvegarde = models.CharField(blank=True)
    adresse = models.CharField(blank=True)
    prenom = models.CharField(blank=True)
    telephone = models.CharField(max_length=15, blank=True)
    cv_original_name = models.CharField(
        blank=False)  # Champs requis
    matches = models.JSONField(blank=False, default=None)


    def __str__(self):
        return f'{self.prenom} {self.nom} - Campagne: {self.campagne.nom}'