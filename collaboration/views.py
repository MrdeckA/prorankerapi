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
    
    
    def get(self, request, *args, **kwargs):
        try:
            inviteur_id = request.GET.get('inviteur')

            if inviteur_id is None:
                return Response({"message": "Paramètre 'inviteur' manquant dans la requête."}, status=status.HTTP_400_BAD_REQUEST)
            
            
            invite_id = request.GET.get('invite')
            email = request.GET.get('email')
            statut_invitation = request.GET.get('statut_invitation')

            if invite_id is None and email is None:
                return Response({"message": "Paramètre 'email' ou 'invite' requis"}, status=status.HTTP_400_BAD_REQUEST)
            
            role = request.GET.get('role')

            if role is None:
                return Response({"message": "Paramètre 'role' manquant dans la requête."}, status=status.HTTP_400_BAD_REQUEST)
            
            
            if(inviteur_id == invite_id):
                return Response({"message": "L'inviteur et l'invite doivent être différent."}, status=status.HTTP_400_BAD_REQUEST)
            
            
           

                
            existing_collaboration = Collaboration.objects.filter(inviteur_id=inviteur_id, invite_id=invite_id).exists()
            
            if(existing_collaboration):
                return Response({"message": "La collaboration existe déjà"}, status=status.HTTP_409_CONFLICT)
            
            inviteur =  get_object_or_404(User, id=inviteur_id)    
            
            
            if(inviteur.email == email):
                return Response({"message": "L'inviteur et l'invite doivent être différent."}, status=status.HTTP_400_BAD_REQUEST)


            if(email is not None):
                
                
              
                
                
                print(f"New user Email sent to {email}")

                # Envoyez l'e-mail de confirmation ici (utilisez Django's Emaildetail ou un package d'envoi d'e-mails tiers)
                sujet = 'PRORANKER - Demande de collaboration'
                url = f'http://localhost:3000/auth/register?inviteur={str(inviteur_id)}&role={role}&email={email}' 
                de = '<mrdeck30@gmail.com>'
                destinataires = [email]
                html_message = f'''
                    <html>
                    <head>
                        <!-- Ajoutez le lien vers Bootstrap CSS -->
                        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
                    </head>
                    <body>
                        <div class="container">
                            <div class="jumbotron">
                                <h4 class="display-4">Bonjour,</h4>
                                <p class="lead">Vous avez été invité par {inviteur.nom_complet} à collaborer sur PRORANKER.</p>
                                <p class="lead">Vous pouvez vous inscrire et accéder à votre dashboard en utilisant l\'URL.</p>
                                <hr class="my-4">
                                <p class="lead">
                                    <a class="btn btn-primary btn-lg" href="{url}" role="button">Inscription</a>
                                </p>
                                <p class="text-muted">Merci !</p>
                            </div>
                        </div>
                    </body>
                    </html>
                '''

                send_mail(subject=sujet, message='', html_message=html_message, from_email=de, recipient_list=destinataires, fail_silently=False)
                return Response({ "message" : "Invitation Envoyée avec succcès" }, status=status.HTTP_200_OK)

                
            else:         
                invite =  get_object_or_404(User, id=invite_id)    
            
                newCollaboration = Collaboration()
                newCollaboration.inviteur =inviteur
                newCollaboration.invite =invite
                newCollaboration.role = role
                
                if(statut_invitation == "Acceptée"):
                    newCollaboration.statut_invitation = "Acceptée"
                
                newCollaboration.save()
                
                
                
                print(f"Email sent to {invite.email}")
                
                # url = 'http://localhost:3000/auth/register?inviteur+' + str(inviteur_id)

                
                # Envoyez l'e-mail de confirmation ici (utilisez Django's Emaildetail ou un package d'envoi d'e-mails tiers)
                sujet = 'PRORANKER - Demande de collaboration'
                url = 'http://localhost:3000/dashboard'
                message = f'Bonjour.\n Vous avez été invité par {inviteur.nom_complet} à collaborer sur PRORANKER. Vous pouvez accéder à votre dashboard en utilisant l\'URL ' + url
                de = '<mrdeck30@gmail.com>'
                destinataires = [invite.email]
                html_message = f'''
                    <html>
                    <head>
                        <!-- Ajoutez le lien vers Bootstrap CSS -->
                        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
                    </head>
                    <body>
                        <div class="container">
                            <div class="jumbotron">
                                <h4 class="display-4">Bonjour,</h4>
                                <p class="lead">Vous avez été invité par {inviteur.nom_complet} à collaborer sur PRORANKER.</p>
                                <hr class="my-4">
                                <p class="lead">
                                    <a class="btn btn-primary btn-lg" href="{url}" role="button">Accepter l'invitation</a>
                                </p>
                                <p class="text-muted">Merci !</p>
                            </div>
                        </div>
                    </body>
                    </html>
                '''


                send_mail(subject=sujet, message=html_message, html_message=html_message, from_email=de, recipient_list=destinataires, fail_silently=False)
                return Response({ "message" :"Invitation Envoyée avec succcès", "collaboration" : CollaborationSerializer(newCollaboration).data }, status=status.HTTP_200_OK)

            
            # newCollaboration.save()
            
            
            # return JsonResponse({"response": CampagneSerializer(campagne).data})
        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)