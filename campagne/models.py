from django.db import models
from user.models import User

# Create your models here.

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