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




# Create your views here.
class CampagneListeView(generics.ListCreateAPIView):
    queryset = Campagne.objects.all()
    serializer_class = CampagneSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CampagneFilter
    permission_classes = [IsAuthenticated, AllPermission]

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
                return Response({"error": "Paramètre 'campagne' manquant dans la requête."}, status=status.HTTP_400_BAD_REQUEST)

        
            chain = CampagneConfig.chain

            campagne = get_object_or_404(Campagne, id=campagne_id)
            poste = f"{campagne.description_poste} {campagne.intitule_poste}"
            # print(json.loads(campagne.files)[0])
            campagne_files = json.loads(campagne.files)

            result_poste = chain.invoke(poste)

            scores = {}

        
            threads = []
            for campagne_file in campagne_files:
                nom_fichier = f"./{campagne_file['saving_name']}"
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
                nom_fichier = f"./{campagne_file['saving_name']}"
                scores[nom_fichier] = calculating_score_for_a_andidate(
                    results_one[nom_fichier], campagne,  result_poste, texts[nom_fichier], request, nom_fichier)
                print(f"done for {nom_fichier}")

            # rs = calculating_score_for_a_andidate(
            #     chain, campagne,  result_poste, request, "./uploads/cv23.pdf")

            return JsonResponse({ "response" : scores})
            # return JsonResponse({"response": CampagneSerializer(campagne).data})
        except Exception as e:
            print(e)
            return JsonResponse({'message': str(e)})

    


    
    

    



class CampagneDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Campagne.objects.all()
    serializer_class = CampagneSerializer
    permission_classes = [IsAuthenticated, AllPermission]
