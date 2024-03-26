from django.db import models
from user.models import User
import uuid
# Create your models here.
class Collaboration(models.Model):
    inviteur = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='collaborations_envoyees')
    invite = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='collaborations_recues')
    # Vous pouvez ajuster la longueur en fonction de vos besoins
    role = models.CharField(max_length=255, default="")

    def __str__(self):
        return f'Collaboration - Inviteur: {self.inviteur.id} - Invite: {self.invite.id} - Rôle: {self.role}'


