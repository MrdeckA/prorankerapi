from rest_framework import serializers
from user.models import User

class UserSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = User
        fields = '__all__'
        
class ObtainTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
class UserCreateSerializer(serializers.ModelSerializer):
    
    is_admin = serializers.BooleanField(required=False)
    nom = serializers.CharField(required=False)
    prenom = serializers.CharField(required=False)
    
    class Meta:
        model = User
        fields = ['email', 'is_admin', 'nom', 'prenom', 'password']
        
class UserManageSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(required=False)
    is_admin = serializers.BooleanField(required=False)
    nom = serializers.CharField(required=False)
    prenom = serializers.CharField(required=False)
    password = serializers.CharField(required=False)

    
    class Meta:
        model = User
        fields = ['email', 'is_admin', 'nom', 'prenom', 'password']