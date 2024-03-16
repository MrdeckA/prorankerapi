from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain
import fitz
api_key = "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"


def extract_ner_from_resume_text(resume_text: str):
    # Schéma des entités à extraire
    schema = {
        "properties": {
            "nom": {"type": "string"},
            "email": {"type": "string"},
            "experiences": {"type": "array", "items": {"type": "string"}},
            "diplomes": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["nom", "email"]
    }

    # clé API openAI

    # # Initialisation du modèle gpt-3.5-turbo
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", api_key=api_key)

    # Création de la chaîne d'extraction
    chain = create_extraction_chain(schema, llm)

    # Exécution de la chaîne sur le texte du CV
    result = chain.invoke(resume_text)['text']

    nom = result[0].get("nom", "")
    email = result[0].get('email', "")
    experiences = result[0].get('experiences', [])
    diplomes = result[0].get("diplomes", [])
    telephone = result[0].get("telephone", "")
    competences = result[0].get("competences", [])
    outils = result[0].get("outils", [])
    langues = result[0].get("langues", [])
    certifications = result[0].get("certifications", [])
    print(result[0])
    
nom_fichier = f"./cv19.pdf"
doc = fitz.open(nom_fichier)
text = "".join(page.get_text() for page in doc)
doc.close()
extract_ner_from_resume_text(text)