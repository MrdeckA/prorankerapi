from django.shortcuts import render
from .apps import CampaignConfig
# Create your views here.
# views.py
import sys
import fitz
from rest_framework import generics
from .models import Campagne, Candidat, Collaborateur
from .serializers import CampagneSerializer, CandidatSerializer, CollaborateurSerializer
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import UploadedFile
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
import base64
import requests
import os
from django.views import View
from django.utils.decorators import method_decorator
import json
from rest_framework.decorators import api_view

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

from django_filters import rest_framework as filters
from .filters import CollaborateurFilter, CampagneFilter, CandidatFilter


def download_and_save_cv(data_urls):
    try:
        # Dossier de destination
        upload_folder = "uploads"

        # Crée le dossier s'il n'existe pas
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        for i, data_url in enumerate(data_urls, start=1):
            # Crée un nom de fichier unique
            filename = f"cv_{i}.pdf"
            save_path = os.path.join(upload_folder, filename)

            # Télécharge les données à partir du data_url
            response = requests.get(data_url)

            # Vérifie si la requête a réussi (code 200)
            if response.status_code == 200:
                # Enregistre le fichier dans le dossier /uploads
                with open(save_path, 'wb') as cv_file:
                    cv_file.write(response.content)

                print(
                    f"Fichier {i} téléchargé et enregistré avec succès à : {save_path}")
            else:
                print(
                    f"La requête pour télécharger le fichier {i} a échoué avec le code de statut : {response.status_code}")

    except Exception as e:
        print(
            f"Une erreur s'est produite lors du téléchargement des fichiers : {str(e)}")

# Exemple d'utilisation


class CandidatUpdateCVPathView(APIView):
    def post(self, request, *args, **kwargs):
        campagne_id = request.data.get('campagne_id', None)

        if campagne_id is None:
            return Response({'error': 'campagne_id est requis dans la requête.'}, status=status.HTTP_400_BAD_REQUEST)

        candidats = Candidat.objects.filter(campagne_id=campagne_id)

        for candidat in candidats:
            candidat.cv_path = "new_cv_path 2"
            download_and_save_cv(candidat.cv_data_url)
            candidat.save()

        serializer = CandidatSerializer(candidats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CandidatBulkCreateView(APIView):
    def post(self, request, *args, **kwargs):
        candidats_data = request.data
        candidats_serializer = CandidatSerializer(
            data=candidats_data, many=True)

        if candidats_serializer.is_valid():
            candidats_serializer.save()
            return Response(candidats_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(candidats_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CampagneListeView(generics.ListCreateAPIView):
    queryset = Campagne.objects.all()
    serializer_class = CampagneSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CampagneFilter


class CampagneDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Campagne.objects.all()
    serializer_class = CampagneSerializer


class CandidatListeView(generics.ListCreateAPIView):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CandidatFilter

    def create(self, request, *args, **kwargs):
        cv_file = request.data.get('cv')

        # Vérifiez si le champ 'cv' contient un fichier PDF
        if cv_file and cv_file.content_type == 'application/pdf':
            try:

                # Utilisez PyMuPDF (fitz) pour extraire le texte du PDF
                # doc = fitz.open(cv_file)
                # print(cv_file.content_type)

                # cv_text = " "
                # for page in doc:
                #     cv_text += str(page.get_text())

                # Ajoutez le texte extrait au champ 'cv' dans les données de la requête
                request.data['cv'] = "cv_text"
            except Exception as e:
                return Response({f"detail': 'Erreur lors de l\'extraction du texte du PDF. {e}"}, status=400)

        return super().create(request, *args, **kwargs)


class CandidatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer


def upload_files(request):
    print(request.FILES)
    if request.method == 'POST' and request.FILES:
        uploaded_files = request.FILES.getlist('files')
        uploaded_file_info = []

        for file in uploaded_files:
            # Enregistrez chaque fichier dans la base de données
            uploaded_file = UploadedFile(
                original_filename=file.name, file=file)
            uploaded_file.save()

            # Ajoutez les informations du fichier à la liste de résultats
            uploaded_file_info.append({
                'original_filename': uploaded_file.original_filename,
                'saved_filename': uploaded_file.file.name.split("/")[-1],
                'upload_date': uploaded_file.upload_date.strftime("%Y-%m-%d %H:%M:%S"),
            })

        return JsonResponse({'files': uploaded_file_info})

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


def file_list(request):
    # Récupérez la liste de tous les fichiers enregistrés
    text = "\n \nSenior Web Developer specializing in front end development. \nExperienced with all stages of the development cycle for dynamic \nweb projects. Well-versed in numerous programming languages \nincluding HTML5, PHP OOP, JavaScript, CSS, MySQL. Strong \nbackground in project management and customer relations. \nExperience \n09/2015 to 05/2019 \nWeb Developer -  Luna Web Design, New York \n• Cooperate with designers to create clean interfaces and \nsimple, intuitive interactions and experiences. \n• Develop project concepts and maintain optimal workflow. \n• Work with senior developer to manage large, complex \ndesign projects for corporate clients. \n• Complete detailed programming and development tasks \nfor front end public and internal websites as well as \nchallenging back-end server code. \n• Carry out quality assurance tests to discover errors and \noptimize usability. \nEducation \n2014-2019  \nBachelor of Science: Computer Information Systems -   \nColumbia University, NY \nCertifications \nPHP Framework (certificate): Zend, Codeigniter, Symfony. \nProgramming Languages: JavaScript, HTML5, PHP OOP, CSS, SQL, \nMySQL. \nReferences \nReferences available on request \nPhone: \n+49 800 600 600 \n \nE-Mail:  \nchristoper.morgan@gmail.com \n \nLinkedin: \nlinkedin.com/christopher.morgan \n \nSkill Highlights \n• Skill Highlights \n• Project management \n• Strong decision maker \n• Complex problem solver \n• Creative design \n• Innovative \n• Service-focused \nLanguages \nSpanish – C2 \nChinese – A1 \n \n \nCHRISTOPHER MORGAN \n"

    myNlp = CampaignConfig.nlp
    doc = myNlp(text)
    # doc = myNlp(text)
    # doc = myNlp(text)
    # doc = myNlp(text)
    # doc = myNlp(text)
    # doc = myNlp(text)
    # doc = myNlp(text)
    # doc = myNlp(text)
    # doc = myNlp(text)
    # doc = myNlp(text)
    # doc = myNlp(text)
    # doc = myNlp(text)
    # doc = myNlp(text)
    # doc = myNlp(text)
    # doc = myNlp(text)
    # doc = myNlp(text)
    # doc = myNlp(text)
    # doc = myNlp(text)
    # doc = myNlp(text)
    # doc = myNlp(text)

    files = UploadedFile.objects.all()
    malist = []
    for ent in doc.ents:
        # Écrire le texte et l'étiquette de l'entité dans le fichier
        malist.append(ent)
    print('ok')

    # return Response({'files': files}, status=200)
    return JsonResponse({'ok': str(malist)}, status=200)


class CollaborateurListeView(generics.ListCreateAPIView):
    queryset = Collaborateur.objects.all()
    serializer_class = CollaborateurSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CollaborateurFilter


class CollaborateurDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collaborateur.objects.all()
    serializer_class = CollaborateurSerializer
