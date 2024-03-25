from rest_framework import serializers
from .models import Campagne

class CampagneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campagne
        fields = '__all__'