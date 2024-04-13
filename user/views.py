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
from django.shortcuts import get_object_or_404
from campagne.models import Campagne
from collaboration.models import Collaboration
from candidat.models import Candidat

import json
# Create your views here.

class CreateUserView(mixins.CreateModelMixin, generics.GenericAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def post(self, request, *args, **kwargs):
        
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer)
        
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        nom = serializer.validated_data.get('nom')
        prenom = serializer.validated_data.get('prenom')
        is_admin = serializer.validated_data.get('is_admin')
        
        
        nom_complet = ''
        
        if(nom is not None and prenom is not None):
            nom_complet = f"{prenom} {nom}"

        
        
        
        
        if is_admin is not None:
            user = User.objects.create_superuser(email=email, password=password, nom=nom, prenom=prenom, is_admin=is_admin, nom_complet=nom_complet)
        else:
            user = User.objects.create_user(email=email, password=password, nom=nom, prenom=prenom, nom_complet=nom_complet)
  
        return Response(self.get_serializer(user).data, status=status.HTTP_201_CREATED)
   
   
   
   
class AllUserView(mixins.ListModelMixin, generics.GenericAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated, AllUserPermission]
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)



class UserStatsView(mixins.ListModelMixin, generics.GenericAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ManagePermission]
    # permission_classes = [IsAuthenticated, AllUserPermission]
    
    def get(self, request, id, *args, **kwargs):
        user=  get_object_or_404(User, id=id)
        user_campagnes = Campagne.objects.filter(user_id=user.id)
        user_collaborations = Collaboration.objects.filter(inviteur_id=user.id)
        user_candidats = Candidat.objects.filter(campagne__user_id=user.id)
        files = 0
        for user_campagne in user_campagnes:
            files = files  + len(json.loads(user_campagne.files))
        return Response({ "candidates" : len(user_candidats), "files" : files,  "recruitments" : len(user_campagnes), "collaborators" : len(user_collaborations) }, status=status.HTTP_200_OK)




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

        # user.set_password(user.password)
        
        if email is not None and (request.user.is_admin or request.user == user):
            
            user.email = email
            
        if password is not None and (request.user.is_admin or request.user == user):
            
            user.set_password(password)
            
        if nom is not None and (request.user.is_admin or request.user == user):
            
            user.nom = nom
            user.nom_complet = f"{user.prenom} {nom}"
            
        if prenom is not None and (request.user.is_admin or request.user == user):
            
            user.prenom = prenom
            user.nom_complet = f"{prenom} {user.nom}"

            
        if is_staff is not None and request.user.is_admin:
            user.is_staff = is_staff
            # user.save()
                
        if is_admin is not None and request.user.is_admin:
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
