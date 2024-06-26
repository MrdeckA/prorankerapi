from django.shortcuts import render
from .models import Campagne
from .serializer import CampagneSerializer
from .filters import CampagneFilter
from candidat.filters import CandidatFilter
from collaboration.filters import CollaborationFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.core.files.storage import FileSystemStorage
from rest_framework.response import Response
import json
from rest_framework import status
from rest_framework import mixins, generics, status
from rest_framework.permissions import IsAuthenticated
from .permissions import AllPermission
from .apps import CampagneConfig
from django.shortcuts import get_object_or_404
import fitz
from unidecode import unidecode
import threading
import re
from candidat.models import Candidat

results_one = {}
texts = {}


def invoke_in_thread(text, results_dict, chain, nom_fichier):
    result = chain.invoke(text)
    results_dict[nom_fichier] = result
    texts[nom_fichier] = text



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


def calculating_score_for_a_andidate(result, campagne: Campagne, result_poste, text, request={}, fname='./uploads/CV_Mériadeck_AMOUSSOU_ATUT.pdf'):

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
            chaine) for chaine in json.loads(campagne.certifications)]
    campagne_languages = [normaliser_chaine(
        chaine) for chaine in json.loads(campagne.languages)]
    campagne_skills = [normaliser_chaine(chaine)
                       for chaine in json.loads(campagne.skills)]

    # scoring
    score = 0
    # certifs
    matches = []
    
    
    # méthode à utiliser
    for chaine1 in campagne_certifications:
        for chaine2 in certifications:
            if chaine1 in chaine2:
                matches.append({
                "source" : chaine1,
                "dest" : chaine2,
                })
                
                
                
    for chaine1 in certifications_poste:
        for chaine2 in certifications:
            if chaine1 in chaine2:
                matches.append({
                "source" : chaine1,
                "dest" : chaine2,
                })
                
    for chaine1 in campagne_skills:
        for chaine2 in competences:
            if chaine1 in chaine2:
                matches.append({
                "source" : chaine1,
                "dest" : chaine2,
                })
                
                
    for chaine1 in competences_poste:
        for chaine2 in competences:
            if chaine1 in chaine2:
                matches.append({
                "source" : chaine1,
                "dest" : chaine2,
                })
                
    for chaine1 in campagne_degrees:
        for chaine2 in diplomes:
            if chaine1 in chaine2:
                matches.append({
                "source" : chaine1,
                "dest" : chaine2,
                })
                
    for chaine1 in diplomes_poste:
        for chaine2 in diplomes:
            if chaine1 in chaine2:
                matches.append({
                "source" : chaine1,
                "dest" : chaine2,
                })
                
                
    for chaine1 in campagne_languages:
        for chaine2 in langues:
            if chaine1 in chaine2:
                matches.append({
                "source" : chaine1,
                "dest" : chaine2,
                })
                
    for chaine1 in langues_poste:
        for chaine2 in langues:
            if chaine1 in chaine2:
                matches.append({
                "source" : chaine1,
                "dest" : chaine2,
                })
                
                
                
    # outils
    for chaine1 in campagne_certifications:
        for chaine2 in outils:
            if chaine1 in chaine2:
                matches.append({
                "source" : chaine1,
                "dest" : chaine2,
                })
                
    for chaine1 in campagne_skills:
        for chaine2 in outils:
            if chaine1 in chaine2:
                matches.append({
                "source" : chaine1,
                "dest" : chaine2,
                })
    for chaine1 in certifications_poste:
        for chaine2 in outils:
            if chaine1 in chaine2:
                matches.append({
                "source" : chaine1,
                "dest" : chaine2,
                })
                
    for chaine1 in competences_poste:
        for chaine2 in outils:
            if chaine1 in chaine2:
                matches.append({
                "source" : chaine1,
                "dest" : chaine2,
                })

  

    

    
   
    if score >= 2 : 
        score += len(langues) >= campagne.minimum_number_of_languages
        score += len(experiences) >= campagne.minimum_number_of_experiences
    
  
    score += len(matches)

    data = {
        "score": score,
        # "prediction": result,
        "email": email,
        "nom_complet": nom,
        "telephone": telephone,
        "texte_pdf": text,
        "fichier": fname.lstrip("./uploads/"),
        "matches": matches,
        "poste" : result_poste[0],
        "cv" : result[0]
    }

    return data





# Create your views here.
class CampagneListeView(generics.ListCreateAPIView):
    queryset = Campagne.objects.all()
    serializer_class = CampagneSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CampagneFilter
    







class CampagneAddFileView(generics.RetrieveUpdateAPIView):
    queryset = Campagne.objects.all()
    serializer_class = CampagneSerializer

    def put(self, request, *args, **kwargs):
        try:
            # Retrieve the ID of the campaign from the URL kwargs
            campagne_id = kwargs.get('pk')
            
            res = json.loads(request.data.get('model'))

            
            # Retrieve the existing campaign instance based on the ID
            instance = Campagne.objects.get(id=campagne_id)

            # Handle the uploaded file
            fichier = request.FILES.get('file')  # Assuming the file is sent as 'file'
            
            if fichier:
                # Save the file to the filesystem
                saving_name = FileSystemStorage("./uploads").get_available_name(fichier.name)
                storage = FileSystemStorage("./uploads")
                storage.save(saving_name, fichier)

                original_name = fichier.name

                # Load existing files and append the new file
                saved_files = json.loads(instance.files) if instance.files else []
                saved_file = {
                    'original_name': original_name,
                    'saving_name': saving_name,
                    'email': res.get('email', ''),
                    'nom_complet': res.get('nom_complet', ''),
                }
                saved_files.append(saved_file)
                instance.files = json.dumps(saved_files)
                
                
                print(instance)

                # Save the instance with the updated files
                instance.save()

                return Response({'campagne': CampagneSerializer(instance).data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No file was provided.'}, status=status.HTTP_400_BAD_REQUEST)

        except Campagne.DoesNotExist:
            return Response({'message': 'Campaign not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class CampagneRankingView(generics.ListCreateAPIView):
    queryset = Campagne.objects.all()
    serializer_class = CampagneSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CampagneFilter
    permission_classes = [IsAuthenticated, AllPermission]
    
    
    def get(self, request, *args, **kwargs):
        try:

            campagne_id = request.GET.get('campagne')

            if campagne_id is None:
                return Response({"message": "Paramètre 'campagne' manquant dans la requête."}, status=status.HTTP_400_BAD_REQUEST)

        
            chain = CampagneConfig.chain

            campagne = get_object_or_404(Campagne, id=campagne_id)
            poste = f"{campagne.description_poste} {campagne.intitule_poste}"
            # print(json.loads(campagne.files)[0])
            campagne_files = json.loads(campagne.files)

            result_poste = chain.invoke(poste)

            scores = {}

        
            threads = []
            for campagne_file in campagne_files:
                nom_fichier = f"./uploads/{campagne_file['saving_name']}"
                doc = fitz.open(nom_fichier)
                text = "".join(page.get_text() for page in doc)
                doc.close()
                        
                thread = threading.Thread(target=invoke_in_thread, args=(text, results_one, chain, nom_fichier))
                threads.append(thread)
                thread.start()

            # Attendre que tous les threads se terminent
            for thread in threads:
                thread.join()


            for campagne_file in campagne_files:
                nom_fichier = f"./uploads/{campagne_file['saving_name']}"
                scores[nom_fichier] = calculating_score_for_a_andidate(
                    results_one[nom_fichier], campagne,  result_poste, texts[nom_fichier], request, nom_fichier)
                print(f"done for {nom_fichier}")
                
                
                


            scores_keys = scores.keys()
            for score_key in scores_keys:
                candidat = Candidat()
                candidat.campagne = campagne
                candidat.nom_complet = scores[score_key]["nom_complet"]
                candidat.email = scores[score_key]["email"]
                candidat.score = scores[score_key]["score"]
                candidat.texte_pdf = scores[score_key]["texte_pdf"]
                candidat.telephone = scores[score_key]["telephone"]
                candidat.fichier = scores[score_key]["fichier"]
                candidat.fichier_sauvegarde = score_key
                candidat.matches = scores[score_key]["matches"]
                candidat.save()

            # rs = calculating_score_for_a_andidate(
            #     chain, campagne,  result_poste, request, "./uploads/cv23.pdf")
            
            

            return Response({ "response" : scores}, status=status.HTTP_200_OK)
            # return JsonResponse({"response": CampagneSerializer(campagne).data})
        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




    


    
    

    



class CampagneDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Campagne.objects.all()
    serializer_class = CampagneSerializer
    permission_classes = [AllPermission]
