# serializers.py

from rest_framework import serializers
from .models import Campagne, Candidat, Collaborateur
from django.contrib.auth.models import User


class CampagneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campagne
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CandidatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidat
        fields = '__all__'


class CollaborateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collaborateur
        fields = '__all__'
