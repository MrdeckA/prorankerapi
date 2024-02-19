from django.apps import AppConfig
import spacy
from functools import lru_cache


class CampaignConfig(AppConfig):
    @staticmethod
    # Utilisez maxsize=None pour un cache de taille illimitée
    @lru_cache(maxsize=None)
    def load_nlp_model(model_path):
        return spacy.load(model_path)

    default_auto_field = "django.db.models.BigAutoField"
    name = "campaign"
    # to do
    # Charger le modèle spaCy lors de la première utilisation et le mettre en cache
    nlp = load_nlp_model("./campaign/sauvegarde_model_best")

    # Charger le modèle spaCy pour le français en grande taille
    spacy_nlp = load_nlp_model("fr_core_news_sm")

    # def ready(self):
    # Chargez votre modèle spaCy ou exécutez d'autres actions au démarrage de l'application
    # self.nlp = nlp
