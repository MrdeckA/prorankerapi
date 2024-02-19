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

    fname = './uploads/Alice Clark CV.pdf'
    doc = fitz.open(fname)
    text = " "
    for page in doc:
        text = text + str(page.get_text())
    prediction1 = CampaignConfig.nlp(text)
    prediction2 = CampaignConfig.spacy_nlp(text)
    descriptionPredicted1 = CampaignConfig.spacy_nlp(
        campagne.description_poste)
    descriptionPredicted2 = CampaignConfig.spacy_nlp(
        campagne.description_poste)
    intitulePostePredicted1 = CampaignConfig.spacy_nlp(
        campagne.intitule_poste)
    intitulePostePredicted2 = CampaignConfig.spacy_nlp(
        campagne.intitule_poste)

    # descriptionPredicted = nl

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
    skills = []
    minimum_number_of_languages = []
    minimum_number_of_experiences = []
    minimum_number_of_years_of_experience = []
    minimum_degree = []
    has_awards = []
    has_certifications = []
    awards = []
    certifications = []
    experiences = []
    degree = []
    descriptions = []
    intitules = []

    # One
    for ent in prediction1.ents:
        # Écrire le texte et l'étiquette de l'entité dans le fichier
        print(f"{ent.text}  ->>>  {ent.label_}\n")

    predict1 = []
    for ent in prediction1.ents:
        # Écrire le texte et l'étiquette de l'entité dans le fichier
        ligne = f"{ent.text}  ->>>  {ent.label_}\n"
        predict1.append(ligne)
        if ent.label_ == 'SKILLS':
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

    predict2 = []
    for ent in prediction2.ents:
        # Écrire le texte et l'étiquette de l'entité dans le fichier
        ligne = f"{ent.text}  ->>>  {ent.label_}\n"
        predict2.append(ligne)
        if ent.label_ == 'MISC':
            globalPredictionMisc.append(ent.text)
        if ent.label_ == 'ORG':
            globalPredictionORG.append(ent.text)

    # Two

    descriptionPredict1 = []
    for ent in descriptionPredicted1.ents:
        # Écrire le texte et l'étiquette de l'entité dans le fichier
        ligne = f"{ent.text}  ->>>  {ent.label_}\n"
        descriptionPredict1.append(ligne)
        if ent.label_ == 'SKILLS':
            descriptionPredictionSkills.append(ent.text)

    descriptionPredict2 = []
    for ent in descriptionPredicted2.ents:
        # Écrire le texte et l'étiquette de l'entité dans le fichier
        ligne = f"{ent.text}  ->>>  {ent.label_}\n"
        descriptionPredict2.append(ligne)
        if ent.label_ == 'MISC':
            descriptionPredictionMisc.append(ent.text)
        if ent.label_ == 'ORG':
            descriptionPredictionORG.append(ent.text)

    # Three

    intitulePostePredict1 = []
    for ent in intitulePostePredicted1.ents:
        # Écrire le texte et l'étiquette de l'entité dans le fichier
        ligne = f"{ent.text}  ->>>  {ent.label_}\n"
        intitulePostePredict1.append(ligne)
        if ent.label_ == 'SKILLS':
            intitulePostePredictionSkills.append(ent.text)

    intitulePostePredict2 = []
    for ent in intitulePostePredicted2.ents:
        # Écrire le texte et l'étiquette de l'entité dans le fichier
        ligne = f"{ent.text}  ->>>  {ent.label_}\n"
        intitulePostePredict2.append(ligne)
        if ent.label_ == 'MISC':
            intitulePostePredictionMisc.append(ent.text)
        if ent.label_ == 'ORG':
            intitulePostePredictionORG.append(ent.text)

    # return JsonResponse({"texte_pdf": CampagneSerializer(campagne).data})

    descriptions.extend(descriptionPredictionSkills)
    descriptions.extend(descriptionPredictionORG)
    descriptions.extend(descriptionPredictionMisc)
    intitules.extend(intitulePostePredictionMisc)
    intitules.extend(intitulePostePredictionORG)
    intitules.extend(intitulePostePredictionMisc)

    return JsonResponse({"descriptions": descriptions, "intitules": intitules, "degree": degree, "experiences": experiences, "certifications": certifications, "awards": awards, "languages": languages, "email": email, "nom_complet": nom_complet, "globalPredictionMisc": globalPredictionMisc, "globalPredictionORG": globalPredictionORG,  "globalPredictionSkills": globalPredictionSkills, "descriptionPredictionORG": descriptionPredictionORG, "descriptionPredictionMisc": descriptionPredictionMisc, "descriptionPredictionSkills": descriptionPredictionSkills, "intitulePostePredictionORG": intitulePostePredictionORG,  "intitulePostePredictionMisc": intitulePostePredictionMisc, "intitulePostePredictionSkills": intitulePostePredictionSkills, "texte_pdf": text, 'prediction1': predict1, 'prediction2': predict2, 'description1': descriptionPredict1, 'description2': descriptionPredict2, 'intitulePostePredict1': intitulePostePredict1, 'intitulePostePredict2': intitulePostePredict2})


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
