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

    fname = './uploads/CV18.pdf'
    doc = fitz.open(fname)
    text = " "
    for page in doc:
        text = text + str(page.get_text())
    prediction1 = CampaignConfig.my_nlp(text)
    prediction2 = CampaignConfig.spacy_nlp(text)
    descriptionPredicted1 = CampaignConfig.my_nlp(campagne.description_poste)
    descriptionPredicted2 = CampaignConfig.spacy_nlp(
        campagne.description_poste)
    intitulePostePredicted1 = CampaignConfig.my_nlp(campagne.intitule_poste)
    intitulePostePredicted2 = CampaignConfig.spacy_nlp(campagne.intitule_poste)

    globalPredictionSkills = []
    globalPredictionMisc = []
    globalPredictionORG = []
    descriptionPredictionSkills = []
    descriptionPredictionMisc = []
    descriptionPredictionORG = []
    intitulePostePredictionSkills = []
    intitulePostePredictionMisc = []
    intitulePostePredictionORG = []
    nom_complet = ""
    email = ""
    languages = []
    awards = []
    certifications = []
    experiences = []
    degree = []
    descriptions = []
    intitules = []
    predictions = []

    # One
    for ent in prediction1.ents:

        if ent.label_ == 'SKILLS' or ent.label_ == 'DESIGNATION' or ent.label_ == 'WORKED AS' or ent.label_ == 'COMPANIES WORKED AT':
            globalPredictionSkills.append(ent.text)
        if ent.label_ == 'NAME':
            nom_complet = ent.text
        if ent.label_ == 'EMAIL ADDRESS':
            email = ent.text
        if ent.label_ == 'LANGUAGE':
            languages.append(ent.text)
        if ent.label_ == 'YEARS OF EXPERIENCE':
            experiences.append(ent.text)
        if ent.label_ == 'DEGREE':
            degree.append(ent.text)
        if ent.label_ == 'AWARDS':
            awards.append(ent.text)
        if ent.label_ == 'CERTIFICATION':
            certifications.append(ent.text)

    for ent in prediction2.ents:
        if ent.label_ == 'MISC':
            globalPredictionMisc.append(ent.text)
        if ent.label_ == 'ORG':
            globalPredictionORG.append(ent.text)

    # Two

    for ent in descriptionPredicted1.ents:
        if ent.label_ == 'SKILLS':
            descriptionPredictionSkills.append(ent.text)

    for ent in descriptionPredicted2.ents:
        if ent.label_ == 'MISC':
            descriptionPredictionMisc.append(ent.text)
        if ent.label_ == 'ORG':
            descriptionPredictionORG.append(ent.text)

    # Three

    for ent in intitulePostePredicted1.ents:
        if ent.label_ == 'SKILLS':
            intitulePostePredictionSkills.append(ent.text)

    for ent in intitulePostePredicted2.ents:
        if ent.label_ == 'MISC':
            intitulePostePredictionMisc.append(ent.text)
        if ent.label_ == 'ORG':
            intitulePostePredictionORG.append(ent.text)

    descriptions.extend(descriptionPredictionSkills)
    descriptions.extend(descriptionPredictionORG)
    descriptions.extend(descriptionPredictionMisc)
    intitules.extend(intitulePostePredictionMisc)
    intitules.extend(intitulePostePredictionORG)
    intitules.extend(intitulePostePredictionMisc)
    predictions.extend(globalPredictionMisc)
    predictions.extend(globalPredictionORG)
    predictions.extend(globalPredictionSkills)
    description_intitule = []
    description_intitule.extend(descriptions)
    description_intitule.extend(intitules)

    description_intitule = [normaliser_chaine(
        chaine) for chaine in description_intitule]
    predictions = [normaliser_chaine(
        chaine) for chaine in predictions]

    # Initialiser la variable de score
    score = 0

    for chaine1 in description_intitule:
        if any(chaine1 in chaine2 for chaine2 in predictions):
            score += 1

    # language
    languages_count = len(languages)
    campagne_languages = [normaliser_chaine(
        chaine) for chaine in campagne.languages.split(',')]
    languages = [normaliser_chaine(
        chaine) for chaine in languages]

    for chaine1 in campagne_languages:
        if any(chaine1 in chaine2 for chaine2 in languages):
            score += 1

    # skills
    campagne_skills = [normaliser_chaine(
        chaine) for chaine in campagne.skills.split(',')]

    for chaine1 in campagne_skills:
        if any(chaine1 in chaine2 for chaine2 in predictions):
            score += 1
    # skills end

    experiences_count = len(experiences)
    awards_count = len(awards)
    certifications_count = len(certifications)

    if awards_count > 0:
        score += 1
    if certifications_count > 0:
        score += 1

    if experiences_count >= campagne.minimum_number_of_experiences:
        score += 1
    if languages_count >= campagne.minimum_number_of_languages:
        score += 1

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

    # To do next time
    for chaine1 in [normaliser_chaine(
            chaine) for chaine in diplomes[campagne.minimum_degree]]:
        if any(chaine1 in chaine2 for chaine2 in [normaliser_chaine(
                chaine) for chaine in degree]):
            score += 1

    # Afficher le score
    print("Score:", score)

    return JsonResponse({"score": score, "description_intitule": description_intitule, "intitules": intitules, "predictions": predictions, "degree": degree, "experiences": experiences, "certifications": certifications, "awards": awards, "languages": languages, "email": email, "nom_complet": nom_complet, "globalPredictionMisc": globalPredictionMisc, "globalPredictionORG": globalPredictionORG,  "globalPredictionSkills": globalPredictionSkills, "descriptionPredictionORG": descriptionPredictionORG, "descriptionPredictionMisc": descriptionPredictionMisc, "descriptionPredictionSkills": descriptionPredictionSkills, "intitulePostePredictionORG": intitulePostePredictionORG,  "intitulePostePredictionMisc": intitulePostePredictionMisc, "intitulePostePredictionSkills": intitulePostePredictionSkills, "texte_pdf": text})


def normaliser_chaine(chaine):
    # Supprimer les espaces
    chaine = chaine.replace(" ", "")

    # Convertir en minuscules
    chaine = chaine.lower()

    # Supprimer les caractères spéciaux
    # chaine = re.sub(r'[^a-zA-Z]', '', chaine)

    # Supprimer les traits d'union ou les points
    chaine = chaine.replace("-", "").replace(".", "")

    # Supprimer les chiffres et les versions
    chaine = re.sub(r'\d+(\.\d+)?', '', chaine)

    # Remplacer les caractères accentués par leur forme sans accent
    chaine = unidecode(chaine)

    # Supprimer les apostrophes et les '/'
    chaine = chaine.replace("'", "").replace("/", "")

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
