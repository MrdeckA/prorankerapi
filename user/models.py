from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
# Create your models here.


class MonUserManager(BaseUserManager):
    def create_user(self, email, password, nom, prenom, **extra_fields):
        if not email:
            raise ValueError('L\'adresse e-mail est obligatoire !')
        if not password:
            raise ValueError('Le mot de passe est obligatoire !')
        if not nom:
            raise ValueError('Le nom est obligatoire !')
        if not prenom:
            raise ValueError('Le prénom est obligatoire !')
    
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
            raise ValueError('Le superutilisateur doit avoir is_admin=True.')

        return self.create_user(email=email, password=password, nom=nom, prenom=prenom, **extra_fields)
    




class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    nom = models.TextField(default="")
    prenom = models.TextField(default="")
    email_valid = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    objects = MonUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']

    def __str__(self):
        return self.email