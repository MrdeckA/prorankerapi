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




# Create your views here.
class CreateUserView(mixins.CreateModelMixin, generics.GenericAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def post(self, request):
        
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        is_admin = serializer.validated_data.get('is_admin')
        
        if is_admin is not None:
            user = User.objects.create_user(email=email, password=password, is_admin=is_admin)
        elif is_admin is None:
            user = User.objects.create_user(email=email, password=password)
        else:
            return Response(({'detail':'Vous devez choisir un rôle pour l\'utilisateur.'}), status=status.HTTP_400_BAD_REQUEST)
        
        # # Envoyez l'e-mail de confirmation ici (utilisez Django's Emaildetail ou un package d'envoi d'e-mails tiers)
        # sujet = 'Confirmation de l\'adresse mail.'
        # url = 'http://127.0.0.1:8000/api/v1/user/mail-verification/' + str(user.id)
        # message = 'Merci de vous être inscrit sur notre site.\n Veuillez vérifier votre addresse mail sur l\'endpoint: ' + url
        # de = 'votre@email.com'
        # destinataires = [email]

        # send_mail(sujet, message, de, destinataires, fail_silently=False)
        
        return Response((self.serializer_class(user).data), status=status.HTTP_200_OK)
   
   
   
   
class AllUserView(mixins.ListModelMixin, generics.GenericAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated, AllUserPermission]
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
