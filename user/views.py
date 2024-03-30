from django.shortcuts import render
from django.core.mail import send_mail
from django.core.exceptions import ValidationError

from rest_framework.response import Response
from rest_framework import status, views
from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticated

from user.serializer import UserSerializer, ObtainTokenSerializer, UserCreateSerializer, UserManageSerializer
# from user.authentication import JWTAuthentication
from user.models import User
# from user.permissions import AllUserPermission, ManagePermission
from user.authentication import JWTAuthentication
from .permissions import ManagePermission




# Create your views here.

class CreateUserView(mixins.CreateModelMixin, generics.GenericAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def post(self, request, *args, **kwargs):
        
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        nom = serializer.validated_data.get('nom')
        prenom = serializer.validated_data.get('prenom')
        is_admin = serializer.validated_data.get('is_admin')
        
        if is_admin is not None:
            user = User.objects.create_superuser(email=email, password=password, nom=nom, prenom=prenom, is_admin=is_admin)
        else:
            user = User.objects.create_user(email=email, password=password, nom=nom, prenom=prenom,)
  
        return Response(self.get_serializer(user).data, status=status.HTTP_201_CREATED)
   
   
   
   
class AllUserView(mixins.ListModelMixin, generics.GenericAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated, AllUserPermission]
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)




class ObtainTokenView(views.APIView):
    
    serializer_class = ObtainTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'E-mail ou mot de passe invalide !'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            return Response({'detail': 'E-mail ou mot de passe invalide !'}, status=status.HTTP_400_BAD_REQUEST)

        # Générer le token JWT
        jwt_token = JWTAuthentication.create_jwt(user)

        return Response({'token': jwt_token, 'user': UserSerializer(user).data})
    
    
    
class ManageView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ManagePermission]

    def put(self, request, id):
        
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'detail':'Utilisateur non identifié.'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            return Response(({'detail':'Identifiant invalide.'}), status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserManageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        nom = serializer.validated_data.get('nom')
        prenom = serializer.validated_data.get('prenom')
        is_staff = serializer.validated_data.get('is_staff')
        is_admin = serializer.validated_data.get('is_admin')
        print(request)

        # user.set_password(user.password)
        update_fields = []
        print(password)
        
        if email is not None and (request.user.is_admin or request.user == user):
            
            user.email = email
            # user.save()
            update_fields.append("email")
            
        if password is not None and (request.user.is_admin or request.user == user):
            
            user.set_password(password)
            # user.save()
            
        if nom is not None and (request.user.is_admin or request.user == user):
            update_fields.append("nom")
            
            user.nom = nom
            # user.save()
            
        if prenom is not None and (request.user.is_admin or request.user == user):
            
            user.prenom = prenom
            update_fields.append("prenom")
            # user.save()
            
        if is_staff is not None and request.user.is_admin:
            update_fields.append("is_staff")
            user.is_staff = is_staff
            # user.save()
                
        if is_admin is not None and request.user.is_admin:
            update_fields.append("is_admin")
            user.is_admin = is_admin
        user.save()
       
        
        return Response((self.serializer_class(user).data), status=status.HTTP_200_OK)
    
    def get(self, request, id):
        
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'detail':'Utilisateur non identifié.'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            return Response(({'detail':'Identifiant invalide.'}), status=status.HTTP_400_BAD_REQUEST)
        
        return Response((self.serializer_class(user).data), status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'detail':'Utilisateur non identifié.'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            return Response(({'detail':'Identifiant invalide.'}), status=status.HTTP_400_BAD_REQUEST)
        
        user.delete()
        
        return Response(({'detail':'Utilisateur supprimé avec succès.'}), status=status.HTTP_200_OK)
