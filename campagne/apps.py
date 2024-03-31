from django.apps import AppConfig
from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain

class CampagneConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "campagne"
    
    
    api_key = "sk-AWPhrgrzegDAyMrgergbvTvrgergf04itkfpT3BlbkFJhRrt4ojmrwx3BmbCmBrnfvfregrgrgegr"
    # api_key = "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"
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
