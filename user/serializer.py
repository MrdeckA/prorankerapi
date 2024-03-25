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
    
    class Meta:
        model = User
        fields = ['email', 'password', 'is_admin']
        
class UserManageSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False)
    is_admin = serializers.BooleanField(required=False)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'is_admin']