from django.shortcuts import render
from rest_framework import generics
from .models import Collaboration
from .filters import CollaborationFilter
from .serializer import CollaborationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import mixins, generics, status
from user.models import User
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

# Create your views here.


class CollaborationListeView(generics.ListCreateAPIView):
    queryset = Collaboration.objects.all()
    serializer_class = CollaborationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CollaborationFilter
    permission_classes = [IsAuthenticated]



class CollaborationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collaboration.objects.all()
    serializer_class = CollaborationSerializer
    permission_classes = [IsAuthenticated]
    
    

        
class CollaborationInvitationView(generics.ListCreateAPIView):
    queryset = Collaboration.objects.all()
    serializer_class = CollaborationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CollaborationFilter
    permission_classes = [IsAuthenticated]
    
    
    def get(self, request, *args, **kwargs):
        try:
            inviteur_id = request.GET.get('inviteur')

            if inviteur_id is None:
                return Response({"message": "Paramètre 'inviteur' manquant dans la requête."}, status=status.HTTP_400_BAD_REQUEST)
            
            
            invite_id = request.GET.get('invite')

            if invite_id is None:
                return Response({"message": "Paramètre 'invite' manquant dans la requête."}, status=status.HTTP_400_BAD_REQUEST)
            
            role = request.GET.get('role')

            if role is None:
                return Response({"message": "Paramètre 'role' manquant dans la requête."}, status=status.HTTP_400_BAD_REQUEST)
            
            
            if(inviteur_id == invite_id):
                return Response({"message": "L'inviteur et l'invite doivent être différent."}, status=status.HTTP_400_BAD_REQUEST)

                
            existing_collaboration = Collaboration.objects.filter(inviteur_id=inviteur_id, invite_id=invite_id).exists()
            
            if(existing_collaboration):
                return Response({"message": "La collaboration existe déjà"}, status=status.HTTP_409_CONFLICT)

                
 
            
            
            inviteur =  get_object_or_404(User, id=inviteur_id)    
            invite =  get_object_or_404(User, id=invite_id)    
        
            newCollaboration = Collaboration()
            newCollaboration.inviteur =inviteur
            newCollaboration.invite =invite
            newCollaboration.role = role
            
            print(f"mail sent to {invite.email}")
            

            
            # Envoyez l'e-mail de confirmation ici (utilisez Django's Emaildetail ou un package d'envoi d'e-mails tiers)
            sujet = 'Confirmation de l\'adresse mail.'
            url = 'http://127.0.0.1:8000/api/v1/user/mail-verification/' + str(inviteur_id)
            message = 'Merci de vous être inscrit sur notre site.\n Veuillez vérifier votre addresse mail sur l\'endpoint: ' + url
            de = '<mrdeck30@gmail.com>'
            destinataires = ['mrdeckamoussou30@gmail.com']

            send_mail(sujet, message, de, destinataires, fail_silently=False)
            
            # newCollaboration.save()
            
            
            return Response(CollaborationSerializer(newCollaboration).data, status=status.HTTP_200_OK)
            # return JsonResponse({"response": CampagneSerializer(campagne).data})
        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)