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
from collections import OrderedDict


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
    scores = {}
    for i in range(1, 24):  # Boucle de cv1.pdf à cv22.pdf
        nom_fichier = f'./uploads/cv{i}.pdf'
        scores[nom_fichier] = lire_contenu_pdfs(fname=nom_fichier)
        print(f"Done for {nom_fichier}")
    valeurs_triees = dict(sorted(scores.items(), key=lambda item: item[1]))

    return JsonResponse({"response": valeurs_triees})


def lire_contenu_pdfs(request={}, fname='./uploads/CV_Mériadeck_AMOUSSOU_ATUT.pdf'):
    campagne = get_object_or_404(Campagne, id=9)
    fname = fname
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

    predictions = []
    descriptions = []
    intitules = []
    nom_complet = ""
    email = ""
    languages = []
    awards = []
    certifications = []
    experiences = []
    degree = []

    for ent in prediction_mon_model.ents:
        if ent.label_ in ('SKILLS', 'DESIGNATION', 'WORKED AS', 'COMPANIES WORKED AT', 'DESIGNATION',
                          'AWARDS',
                          'CERTIFICATION'):
            predictions.append(ent.text)
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
            predictions.append(ent.text)
        elif ent.label_ == 'ORG':
            predictions.append(ent.text)

    for ent in description_prediction_mon_model.ents:
        if ent.label_ == 'SKILLS':
            descriptions.append(ent.text)

    for ent in description_prediction_model_spacy.ents:
        if ent.label_ == 'MISC':
            descriptions.append(ent.text)
        elif ent.label_ == 'ORG':
            descriptions.append(ent.text)

    for ent in intitule_poste_prediction_mon_model.ents:
        if ent.label_ == 'SKILLS':
            intitules.append(ent.text)

    for ent in intitule_poste_prediction_model_spacy.ents:
        if ent.label_ == 'MISC':
            intitules.append(ent.text)
        elif ent.label_ == 'ORG':
            intitules.append(ent.text)

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
        "texte_pdf": text
    }

    return score


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
