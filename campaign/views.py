from django.shortcuts import render
from .apps import CampaignConfig
# Create your views here.
# views.py
import sys
import fitz
from rest_framework import generics
from .models import Campagne, Candidat, Collaboration
from .serializers import CampagneSerializer, CandidatSerializer, CollaborationSerializer, UserSerializer
from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt
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
from .filters import CollaborationFilter, CampagneFilter, CandidatFilter
from django.shortcuts import get_object_or_404
import re
from unidecode import unidecode
from collections import OrderedDict
from utils.main import is_valid_email, recuperer_premiere_email
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from rest_framework.decorators import api_view, parser_classes
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain


class CampagneListeView(generics.ListCreateAPIView):
    queryset = Campagne.objects.all()
    serializer_class = CampagneSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CampagneFilter

    def post(self, request):
        try:
            # print(request.FILES)
            res = json.loads(request.data.get('model'))

            saved_files = []

            for key, fichier in request.FILES.items():
                # Générer un nouveau nom pour le fichier (saving name)
                saving_name = FileSystemStorage().get_available_name(fichier.name)

                # Sauvegarder le fichier avec le nouveau nom
                storage = FileSystemStorage()
                storage.save(saving_name, fichier)

                # Récupérer le nom d'origine du fichier (original name)
                original_name = fichier.name

                # Vous pouvez maintenant utiliser original_name et saving_name comme nécessaire

                saved_file = {}
                saved_file['original_name'] = original_name
                saved_file['saving_name'] = saving_name
                saved_files.append(saved_file)

            newCampagne = Campagne(
                nom=res.get('nom', ''),
                description_poste=res.get('description_poste', ''),
                intitule_poste=res.get('intitule_poste', ''),
                minimum_number_of_languages=res.get(
                    'minimum_number_of_languages', 0),
                minimum_number_of_experiences=res.get(
                    'minimum_number_of_experiences', 0),
                languages=json.dumps(res.get('languages', [])),
                skills=json.dumps(res.get('skills', [])),
                degrees=json.dumps(res.get('degrees', [])),
                certifications=json.dumps(res.get('certifications', [])),
                user_id=res.get('user', ''),
                files=json.dumps(saved_files)
            )
            # print(res.get('nom'))
            newCampagne.save()

            # newCampagne.save()
            # print(request.user)
            # Boucle à travers tous les fichiers dans request.FILES

            return Response({'campagne':  CampagneSerializer(newCampagne).data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CampagneDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Campagne.objects.all()
    serializer_class = CampagneSerializer


class CandidatListeView(generics.ListCreateAPIView):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CandidatFilter


class CandidatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer


class CollaborationListeView(generics.ListCreateAPIView):
    queryset = Collaboration.objects.all()
    serializer_class = CollaborationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CollaborationFilter


class CollaborationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collaboration.objects.all()
    serializer_class = CollaborationSerializer


def make_ranking(request):
    try:
        llm = CampaignConfig.llm

        campagne_id = request.GET.get('campagne')

        if campagne_id is None:
            return JsonResponse({"error": "Paramètre 'campagne' manquant dans la requête."})

        schema = {
            "properties": {
                "nom": {"type": "string"},
                "email": {"type": "string"},
                "telephone": {"type": "string"},
                "experiences": {"type": "array", "items": {"type": "string"}},
                "diplomes": {"type": "array", "items": {"type": "string"}},
                "competences": {"type": "array", "items": {"type": "string"}},
                "outils": {"type": "array", "items": {"type": "string"}},
                "langues": {"type": "array", "items": {"type": "string"}},
                "certifications": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["nom", "email"]
        }

        chain = create_extraction_chain(schema, llm, verbose=True)

        campagne = get_object_or_404(Campagne, id=campagne_id)
        poste = f"{campagne.description_poste} {campagne.intitule_poste}"
        # print(json.loads(campagne.files)[0])
        campagne_files = json.loads(campagne.files)

        result_poste = chain.invoke(poste)

        scores = {}

        results = {}
        # for i in range(3, 20):  # Boucle de cv1.pdf à cv22.pdf
        #     nom_fichier = f'./uploads/cv{i}.pdf'
        #     result = calculating_score_for_a_andidate(
        #         fname=nom_fichier)
        #     # email: data['email'], score: data["score"], nom_complet: data['nom_complet'],

        #     scores[nom_fichier] = result['score']
        #     results[nom_fichier] = result[f'{nom_fichier}']
        #     print(f"Done for {nom_fichier}")

        # valeurs_triees = scores
        # valeurs_triees = dict(sorted(scores.items(), key=lambda item: item[1]))
        # print(result)

        for campagne_file in campagne_files:
            nom_fichier = f"./{campagne_file['saving_name']}"
            scores[nom_fichier] = calculating_score_for_a_andidate(
                chain, campagne,  result_poste, request, nom_fichier)
            print(f"done for {nom_fichier}")

        # rs = calculating_score_for_a_andidate(
        #     chain, campagne,  result_poste, request, "./uploads/cv23.pdf")

        return JsonResponse({"response": scores})
        # return JsonResponse({"response": CampagneSerializer(campagne).data})
    except Exception as e:
        print(e)
        return JsonResponse({'message': str(e)})


def calculating_score_for_a_andidate(chain, campagne: Campagne, result_poste, request={}, fname='./uploads/CV_Mériadeck_AMOUSSOU_ATUT.pdf'):

    fname = fname
    doc = fitz.open(fname)
    text = "".join(page.get_text() for page in doc)
    doc.close()
    print("before")

    result = chain.invoke(text)
    print("after")

    # Exécution de la chaîne sur le texte du CV

    result = result['text']
    # Résultat
    nom = result[0].get("nom", "")
    email = result[0].get('email', "")
    telephone = result[0].get("telephone", "")
    experiences = result[0].get('experiences', [])
    diplomes = result[0].get("diplomes", [])
    competences = result[0].get("competences", [])
    outils = result[0].get("outils", [])
    langues = result[0].get("langues", [])
    certifications = result[0].get("certifications", [])

    # Exécution de la chaîne sur le texte du CV

    result_poste = result_poste['text']
    # Résultat 1
    nom_poste = result_poste[0].get("nom", "")
    experiences_poste = result_poste[0].get('experiences', [])
    diplomes_poste = result_poste[0].get("diplomes", [])
    competences_poste = result_poste[0].get("competences", [])
    outils_poste = result_poste[0].get("outils", [])
    langues_poste = result_poste[0].get("langues", [])
    certifications_poste = result_poste[0].get("certifications", [])

    # # cv
    competences = [normaliser_chaine(chaine) for chaine in competences]
    experiences = [normaliser_chaine(chaine) for chaine in experiences]
    certifications = [normaliser_chaine(chaine) for chaine in certifications]
    langues = [normaliser_chaine(chaine) for chaine in langues]
    outils = [normaliser_chaine(chaine) for chaine in outils]
    diplomes = [normaliser_chaine(chaine) for chaine in diplomes]

    # # extrait de la description du poste
    experiences_poste = [normaliser_chaine(
        chaine) for chaine in experiences_poste]
    diplomes_poste = [normaliser_chaine(chaine) for chaine in diplomes_poste]
    competences_poste = [normaliser_chaine(
        chaine) for chaine in competences_poste]
    outils_poste = [normaliser_chaine(chaine) for chaine in outils_poste]
    langues_poste = [normaliser_chaine(chaine) for chaine in langues_poste]
    certifications_poste = [normaliser_chaine(
        chaine) for chaine in certifications_poste]

    # # campagne
    # campagne_minimum_degree = normaliser_chaine(campagne.minimum_degree)
    campagne_degrees = [normaliser_chaine(
        chaine) for chaine in json.loads(campagne.degrees)]
    campagne_certifications = []
    if (campagne.certifications):
        campagne_certifications = [normaliser_chaine(
            chaine) for chaine in campagne.certifications]
    campagne_languages = [normaliser_chaine(
        chaine) for chaine in json.loads(campagne.languages)]
    campagne_skills = [normaliser_chaine(chaine)
                       for chaine in json.loads(campagne.skills)]

    # scoring
    score = 0
    score += sum(any(chaine1 in chaine2 for chaine2 in certifications)
                 for chaine1 in campagne_certifications)
    score += sum(any(chaine1 in chaine2 for chaine2 in competences)
                 for chaine1 in campagne_skills)
###
    score += sum(any(chaine1 in chaine2 for chaine2 in experiences)
                 for chaine1 in campagne_certifications)
    score += sum(any(chaine1 in chaine2 for chaine2 in outils)
                 for chaine1 in campagne_certifications)
    score += sum(any(chaine1 in chaine2 for chaine2 in competences)
                 for chaine1 in campagne_certifications)

    #

    score += sum(any(chaine1 in chaine2 for chaine2 in experiences)
                 for chaine1 in campagne_skills)
    score += sum(any(chaine1 in chaine2 for chaine2 in outils)
                 for chaine1 in campagne_skills)
    score += sum(any(chaine1 in chaine2 for chaine2 in certifications)
                 for chaine1 in campagne_skills)

###
    score += sum(any(chaine1 in chaine2 for chaine2 in langues)
                 for chaine1 in campagne_languages)
    score += sum(any(chaine1 in chaine2 for chaine2 in diplomes)
                 for chaine1 in campagne_degrees)

    score += len(langues) >= campagne.minimum_number_of_languages
    score += len(experiences) >= campagne.minimum_number_of_experiences

    # descrition + intitule


###

    score += sum(any(chaine1 in chaine2 for chaine2 in experiences_poste)
                 for chaine1 in certifications)
    score += sum(any(chaine1 in chaine2 for chaine2 in certifications_poste)
                 for chaine1 in certifications)

    score += sum(any(chaine1 in chaine2 for chaine2 in outils_poste)
                 for chaine1 in certifications)

    score += sum(any(chaine1 in chaine2 for chaine2 in competences_poste)
                 for chaine1 in certifications)

    #

    score += sum(any(chaine1 in chaine2 for chaine2 in experiences_poste)
                 for chaine1 in experiences)
    score += sum(any(chaine1 in chaine2 for chaine2 in certifications_poste)
                 for chaine1 in experiences)

    score += sum(any(chaine1 in chaine2 for chaine2 in outils_poste)
                 for chaine1 in experiences)

    score += sum(any(chaine1 in chaine2 for chaine2 in competences_poste)
                 for chaine1 in experiences)

    #
    score += sum(any(chaine1 in chaine2 for chaine2 in experiences_poste)
                 for chaine1 in outils)
    score += sum(any(chaine1 in chaine2 for chaine2 in certifications_poste)
                 for chaine1 in outils)

    score += sum(any(chaine1 in chaine2 for chaine2 in outils_poste)
                 for chaine1 in outils)

    score += sum(any(chaine1 in chaine2 for chaine2 in competences_poste)
                 for chaine1 in outils)

    #
    score += sum(any(chaine1 in chaine2 for chaine2 in experiences_poste)
                 for chaine1 in competences)
    score += sum(any(chaine1 in chaine2 for chaine2 in certifications_poste)
                 for chaine1 in competences)

    score += sum(any(chaine1 in chaine2 for chaine2 in outils_poste)
                 for chaine1 in competences)

    score += sum(any(chaine1 in chaine2 for chaine2 in competences_poste)
                 for chaine1 in competences)


###

    score += sum(any(chaine1 in chaine2 for chaine2 in langues_poste)
                 for chaine1 in langues)
    score += sum(any(chaine1 in chaine2 for chaine2 in diplomes_poste)
                 for chaine1 in diplomes)

    score += sum(any(chaine1 in chaine2 for chaine2 in diplomes_poste)
                 for chaine1 in campagne_degrees)

    data = {
        "score": score,
        # "prediction": result,
        "email": email,
        "nom_complet": nom,
        "telephone": telephone,
        "texte_pdf": text,
        "fichier": fname
    }

    return data


def normaliser_chaine(chaine):

    # Convertir en minuscules
    chaine = chaine.lower()

    # Supprimer les chiffres et les versions
    chaine = re.sub(r'\d+(\.\d+)?', '', chaine)

    # Remplacer les caractères accentués par leur forme sans accent
    chaine = unidecode(chaine)

    # Supprimer les apostrophes et les '/' et les espaces
    # Supprimer les traits d'union ou les points
    chaine = chaine.replace("'", "").replace(
        "/", "").replace(" ", "").replace("-", "").replace(".", "").replace(",", "")

    return chaine


def charger_contenu_pdfs(request):
    # Assurez-vous d'ajuster le chemin selon votre structure de fichiers
    dossier_cvs = './uploads/'

    contenu_cvs = []

    for i in range(1, 23):  # Boucle de cv1.pdf à cv22.pdf
        nom_fichier = f'cv{i}.pdf'
        chemin_fichier = os.path.join(dossier_cvs, nom_fichier)

        if os.path.exists(chemin_fichier):
            doc = fitz.open(chemin_fichier)
            texte = " "
            for page in doc:
                texte = texte + str(page.get_text())

            predict = CampaignConfig.nlp(texte)

            print(f"done for cv{i}.pdf")
            predict1 = []

            for ent in predict.ents:
                # Écrire le texte et l'étiquette de l'entité dans le fichier
                ligne = f"{ent.text}  ->>>  {ent.label_}\n"
                predict1.append(ligne)

            contenu_cvs.append({
                "nom_fichier": nom_fichier,
                # "texte_pdf": texte,
                "predict":  predict1
            })
            doc.close()

    return JsonResponse({"contenu_cvs": contenu_cvs})


@api_view(['POST'])
@csrf_exempt
def posting(request):
    try:
        # Boucle à travers tous les fichiers dans request.FILES
        for key, fichier in request.FILES.items():
            # Générer un nouveau nom pour le fichier (saving name)
            saving_name = FileSystemStorage().get_available_name(fichier.name)

            # Sauvegarder le fichier avec le nouveau nom
            storage = FileSystemStorage()
            storage.save(saving_name, fichier)

            # Récupérer le nom d'origine du fichier (original name)
            original_name = fichier.name

            # Vous pouvez maintenant utiliser original_name et saving_name comme nécessaire
            print("Nom d'origine:", original_name)
            print("Nom de sauvegarde:", saving_name)

        return Response({'message': 'Fichiers sauvegardés avec succès.'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # fichier = request.FILES
    # print(request.FILES)
    # parser_classes = [FileUploadParser]

    # # Logique pour sauvegarder le fichier, par exemple avec FileSystemStorage
    # # Vous devrez ajuster cela en fonction de votre logique spécifique
    # # storage = FileSystemStorage()
    # # nom_fichier = storage.save(fichier.name, fichier)

    # return JsonResponse({"contenu_cvs": "contenu_cvs"})


"""
class ListeCampagnesAvecCollaborateurs(APIView):
    def get(self, request, *args, **kwargs):
        # Récupérer l'utilisateur à partir des paramètres de requête
        user_id = self.request.query_params.get('user', None)

        # Vérifier si l'ID de l'utilisateur est fourni dans les paramètres de requête
        if user_id is None:
            return Response({"error": "Paramètre 'user' manquant dans la requête."}, status=400)

        # Récupérer la liste des campagnes pour cet utilisateur
        campagnes = Campagne.objects.filter(
            collaborateurs__user=user_id).distinct()
        # campagnes_sans_collaborateurs = Campagne.objects.filter(
        #     collaborateurs__user=user_id).exclude(collaborateurs__isnull=False).distinct()

        # campagnes_sans_collaborateur = Campagne.objects.filter(
        #     user=user_id, collaborateurs__isnull=True)

        # Initialiser une liste pour stocker les données de chaque campagne
        data_campagnes = []

        # Parcourir les campagnes
        for campagne in campagnes:
            # Récupérer les collaborateurs pour chaque campagne
            collaborateurs = Collaborateur.objects.filter(campagne=campagne)

            for col in collaborateurs:

                # user = User.objects.get(id=col.user)
                # serializer = UserSerializer(user)
                # serialized_user = serializer.data
                col.user_full_name = col.user.get_full_name()

            # Sérialiser les collaborateurs avec le sérialiseur CollaborateurSerializer
            serializer = CollaborateurSerializer(collaborateurs, many=True)
            serialized_collaborateurs = serializer.data

            # Ajouter l'ID de la campagne au dictionnaire
            data_campagne = {
                'id_campagne': campagne.id,
                'nom_campagne': campagne.nom,
                'collaborateurs': serialized_collaborateurs,
                'total': len(serialized_collaborateurs)
            }

            # Ajouter le dictionnaire de la campagne à la liste
            data_campagnes.append(data_campagne)

        return Response(data_campagnes)

"""
# class ListeCampagnesAvecCollaborateurs1(APIView):

#     def get(self, request, *args, **kwargs):
#         # Récupérer les paramètres de requête
#         campagne_id = self.request.query_params.get('campagne_id', None)

#         # Vérifier si les paramètres nécessaires sont fournis dans les paramètres de requête
#         if campagne_id is None:
#             return Response({"error": "Paramètre 'campagne_id' manquant dans la requête."}, status=400)

#         # Récupérer le collaborateur correspondant aux paramètres ou renvoyer une 404
#         collaborateurs = Collaborateur.objects.filter(campagne=campagne_id)

#         for col in collaborateurs:

#             # user = User.objects.get(id=col.user)
#             # serializer = UserSerializer(user)
#             # serialized_user = serializer.data
#             col.user_full_name = col.user.get_full_name()

#         # Sérialiser le collaborateur
#         serializer = CollaborateurSerializer(collaborateurs, many=True)
#         serialized_collaborateurs = serializer.data

#         return Response(serialized_collaborateurs)
