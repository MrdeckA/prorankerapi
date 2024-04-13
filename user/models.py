from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
import uuid

class MonUserManager(BaseUserManager):
    def create_user(self, email, password, nom, prenom, **extra_fields):
        if not email:
            raise ValidationError({'email': 'L\'adresse e-mail est obligatoire !'}, code=status.HTTP_400_BAD_REQUEST)
        if not password:
            raise ValidationError({'password': 'Le mot de passe est obligatoire !'}, code=status.HTTP_400_BAD_REQUEST)
        if not nom:
            raise ValidationError({'nom': 'Le nom est obligatoire !'}, code=status.HTTP_400_BAD_REQUEST)
        if not prenom:
            raise ValidationError({'prenom': 'Le prénom est obligatoire !'}, code=status.HTTP_400_BAD_REQUEST)
    
        email = self.normalize_email(email)
        user = self.model(email=email, nom=nom, prenom=prenom, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    
    def create_superuser(self, email, password, nom, prenom, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        email = self.normalize_email(email)
        
        if extra_fields.get('is_admin') is not True:
            raise ValidationError({'is_admin': 'Le superutilisateur doit avoir is_admin=True.'}, code=status.HTTP_400_BAD_REQUEST)

        return self.create_user(email=email, password=password, nom=nom, prenom=prenom, **extra_fields)
    




class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    nom_complet = models.CharField(max_length=255, default='')
    email_valid = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    objects = MonUserManager()

    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['nom', 'prenom']

    def __str__(self):
        return self.email
