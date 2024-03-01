
from django.contrib import admin
from django.urls import path
from campaign.views import CampagneListeView, CampagneDetailView, CandidatListeView, CandidatDetailView, CollaborateurListeView, CollaborateurDetailView, make_ranking, charger_contenu_pdfs, posting, ListeCampagnesAvecCollaborateurs, ListeCampagnesAvecCollaborateurs1


urlpatterns = [
    path('campagnes/', CampagneListeView.as_view(), name='campagne-liste'),
    path('campagnes/<int:pk>/', CampagneDetailView.as_view(), name='campagne-detail'),
    path('candidats/', CandidatListeView.as_view(), name='candidat-liste'),
    path('candidats/<int:pk>/', CandidatDetailView.as_view(), name='candidat-detail'),
    path('collaborateurs/', CollaborateurListeView.as_view(),
         name='collaborateur-liste'),
    path('collaborateurs/<int:pk>/',
         CollaborateurDetailView.as_view(), name='collaborateur-detail'),
    #     path('prediction/start/',
    #          CollaborateurDetailView.as_view(), name='start-prediction'),
    path('prediction/start/', make_ranking, name='start-prediction'),
    path('posting/', posting, name='posting'),
    path('charger_contenu_pdfs/', charger_contenu_pdfs,
         name='charger_contenu_pdfs'),
    path('liste-campagnes-collaborateurs/', ListeCampagnesAvecCollaborateurs.as_view(),
         name='liste-campagnes-collaborateurs'),
    path('collaborators/campagne', ListeCampagnesAvecCollaborateurs1.as_view(),
         name='get-collaborators-for-campaign'),




]
