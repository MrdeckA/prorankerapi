from django.apps import AppConfig
import spacy
from functools import lru_cache
from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain


class CampaignConfig(AppConfig):
    # @staticmethod
    # Utilisez maxsize=None pour un cache de taille illimitée
    # @lru_cache(maxsize=None)
    # def load_nlp_model(model_path):
    #     return spacy.load(model_path)

    api_key = "sk-AWPhDAyMbvTvf04itkfpT3BlbkFJhRrt4ojmrwx3BmbCmBrnfv"
    # api_key=""

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo",
                     api_key=api_key)
    
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

    chain = create_extraction_chain(schema, llm)

    default_auto_field = "django.db.models.BigAutoField"
    name = "campaign"
    # to do
    # Charger le modèle spaCy lors de la première utilisation et le mettre en cache
    # nlp = load_nlp_model("./campaign/sauvegarde_model_best")

    # Charger le modèle spaCy pour le français en grande taille
    # spacy_nlp = load_nlp_model("fr_core_news_md")

    # my_nlp = nlp

    # def ready(self):
    # Chargez votre modèle spaCy ou exécutez d'autres actions au démarrage de l'application
    # self.nlp = nlp
