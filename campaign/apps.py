from django.apps import AppConfig
import spacy


class CampaignConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "campaign"
    # to do
    # nlp = spacy.load("./campaign/sauvegarde_model")

    # def ready(self):
    # Chargez votre modèle spaCy ou exécutez d'autres actions au démarrage de l'application
    # self.nlp = nlp
