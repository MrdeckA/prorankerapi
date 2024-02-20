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
from django.shortcuts import get_object_or_404
import re
from unidecode import unidecode


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


class CandidatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer


class CollaborateurListeView(generics.ListCreateAPIView):
    queryset = Collaborateur.objects.all()
    serializer_class = CollaborateurSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CollaborateurFilter


class CollaborateurDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collaborateur.objects.all()
    serializer_class = CollaborateurSerializer


def lire_contenu_pdf(request):
    campagne = get_object_or_404(Campagne, id=9)
    fname = './uploads/CV_Mériadeck_AMOUSSOU_ATUT.pdf'
    doc = fitz.open(fname)
    text = "".join(page.get_text() for page in doc)
    doc.close()

    prediction_mon_model = CampaignConfig.my_nlp(text)
    prediction_model_spacy = CampaignConfig.spacy_nlp(text)
    description_prediction_mon_model = CampaignConfig.my_nlp(
        campagne.description_poste)
    description_prediction_model_spacy = CampaignConfig.spacy_nlp(
        campagne.description_poste)
    intitule_poste_prediction_mon_model = CampaignConfig.my_nlp(
        campagne.intitule_poste)
    intitule_poste_prediction_model_spacy = CampaignConfig.spacy_nlp(
        campagne.intitule_poste)

    global_prediction_skills = []
    global_prediction_misc = []
    global_prediction_org = []
    description_prediction_skills = []
    description_prediction_misc = []
    description_prediction_org = []
    intitule_poste_prediction_skills = []
    intitule_poste_prediction_misc = []
    intitule_poste_prediction_org = []
    nom_complet = ""
    email = ""
    languages = []
    awards = []
    certifications = []
    experiences = []
    degree = []

    for ent in prediction_mon_model.ents:
        if ent.label_ in ('SKILLS', 'DESIGNATION', 'WORKED AS', 'COMPANIES WORKED AT'):
            global_prediction_skills.append(ent.text)
        elif ent.label_ == 'NAME':
            nom_complet = ent.text
        elif ent.label_ == 'EMAIL ADDRESS':
            email = ent.text
        elif ent.label_ == 'LANGUAGE':
            languages.append(ent.text)
        elif ent.label_ == 'YEARS OF EXPERIENCE':
            experiences.append(ent.text)
        elif ent.label_ == 'DEGREE':
            degree.append(ent.text)
        elif ent.label_ == 'AWARDS':
            awards.append(ent.text)
        elif ent.label_ == 'CERTIFICATION':
            certifications.append(ent.text)

    for ent in prediction_model_spacy.ents:
        if ent.label_ == 'MISC':
            global_prediction_misc.append(ent.text)
        elif ent.label_ == 'ORG':
            global_prediction_org.append(ent.text)

    for ent in description_prediction_mon_model.ents:
        if ent.label_ == 'SKILLS':
            description_prediction_skills.append(ent.text)

    for ent in description_prediction_model_spacy.ents:
        if ent.label_ == 'MISC':
            description_prediction_misc.append(ent.text)
        elif ent.label_ == 'ORG':
            description_prediction_org.append(ent.text)

    for ent in intitule_poste_prediction_mon_model.ents:
        if ent.label_ == 'SKILLS':
            intitule_poste_prediction_skills.append(ent.text)

    for ent in intitule_poste_prediction_model_spacy.ents:
        if ent.label_ == 'MISC':
            intitule_poste_prediction_misc.append(ent.text)
        elif ent.label_ == 'ORG':
            intitule_poste_prediction_org.append(ent.text)

    descriptions = description_prediction_skills + \
        description_prediction_org + description_prediction_misc
    intitules = intitule_poste_prediction_misc + \
        intitule_poste_prediction_org + intitule_poste_prediction_skills
    predictions = global_prediction_misc + \
        global_prediction_org + global_prediction_skills
    description_intitule = descriptions + intitules

    description_intitule = [normaliser_chaine(
        chaine) for chaine in description_intitule]
    predictions = [normaliser_chaine(chaine) for chaine in predictions]

    # Initialiser la variable de score
    score = sum(any(chaine1 in chaine2 for chaine2 in predictions)
                for chaine1 in description_intitule)

    # language
    languages_count = len(languages)
    campagne_languages = [normaliser_chaine(
        chaine) for chaine in campagne.languages.split(',')]
    languages = [normaliser_chaine(chaine) for chaine in languages]
    score += sum(any(chaine1 in chaine2 for chaine2 in languages)
                 for chaine1 in campagne_languages)

    # skills
    campagne_skills = [normaliser_chaine(chaine)
                       for chaine in campagne.skills.split(',')]
    score += sum(any(chaine1 in chaine2 for chaine2 in predictions)
                 for chaine1 in campagne_skills)

    # autres critères
    experiences_count = len(experiences)
    awards_count = len(awards)
    certifications_count = len(certifications)

    score += awards_count > 0
    score += certifications_count > 0
    score += experiences_count >= campagne.minimum_number_of_experiences
    score += languages_count >= campagne.minimum_number_of_languages

    diplomes = {
        "Diplôme d'études primaires (DEP)": ["DEP", "Diplôme d'études primaires"],
        "Brevet d'études du premier cycle (BEPC)": ["BEPC", "Brevet d'études du premier cycle"],
        "Baccalauréat (BAC)": ["BAC", "Baccalauréat"],
        "Licence (L1, L2, L3)": ["Licence", "L1", "L2", "L3"],
        "Master (M1, M2)": ["Master", "M1", "M2"],
        "Doctorat (Ph.D.)": ["Doctorat", "Ph.D."],
        "Certificat d'aptitude professionnelle (CAP)": ["CAP", "Certificat d'aptitude professionnelle"],
        "Brevet de technicien supérieur (BTS)": ["BTS", "Brevet de technicien supérieur"],
        "Diplôme universitaire de technologie (DUT)": ["DUT", "Diplôme universitaire de technologie"],
        "Certificat universitaire (CU)": ["CU", "Certificat universitaire"],
        "Mastère spécialisé (MS)": ["MS", "Mastère spécialisé"],
        "Agrégation": ["Agrégation"]
    }
    degree = [normaliser_chaine(chaine) for chaine in degree]
    campagne_diplome = [normaliser_chaine(
        chaine) for chaine in diplomes[campagne.minimum_degree]]
    score += any(chaine1 in chaine2 for chaine1 in campagne_diplome for chaine2 in degree)

    data = {
        "score": score,
        "description_intitule": description_intitule,
        "intitules": intitules,
        "predictions": predictions,
        "degree": degree,
        "experiences": experiences,
        "certifications": certifications,
        "awards": awards,
        "languages": languages,
        "email": email,
        "nom_complet": nom_complet,
        "globalPredictionMisc": global_prediction_misc,
        "globalPredictionORG": global_prediction_org,
        "globalPredictionSkills": global_prediction_skills,
        "descriptionPredictionORG": description_prediction_org,
        "descriptionPredictionMisc": description_prediction_misc,
        "descriptionPredictionSkills": description_prediction_skills,
        "intitulePostePredictionORG": intitule_poste_prediction_org,
        "intitulePostePredictionMisc": intitule_poste_prediction_misc,
        "intitulePostePredictionSkills": intitule_poste_prediction_skills,
        "texte_pdf": text
    }

    return JsonResponse({"score": score})


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
        "/", "").replace(" ", "").replace("-", "").replace(".", "")

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
