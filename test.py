# from langchain.chains import create_extraction_chain
# from langchain_openai import ChatOpenAI

# # Texte du CV
from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain
cv_text = """
AMOUSSOU MÉRIADECK

mrdeck30@gmail.com

https://meriadeckamoussou.me

Abomey-Calavi, Bénin

+229 52 74 69 12

Cursus & Formations

Institut de Formation et de Recherche en Informatique (IFRI) / Université d’Abomey-Calavi (UAC)
2020-2023 : Licence en Génie Logiciel (3/3ans) (En instance de soutennce)

Collège Catholique Pierre Joseph de Cloriviere d’Abomey-Calavi

2019-2020 : Baccalauréat série D

Collège Catholique Pierre Joseph de Cloriviere d’Abomey-Calavi

2016-2017 : Brevet d'Etude du Premier Cycle (BEPC)

Langues
Fon : parlé
Français & Anglais : lu, écrit, parlé

Expériences professionnelles
Développeur Web Full Stack Javascript (A distance) : De Octobre 2023 à maintenant

Lieu : Foortina Prime - Parakou
Missions : Développement d'applications web en Vue.js/Nuxt.js et Express.js

Stagiaire, Développeur Web : D'avril 2023 à juin 2023

Lieu : Jilmonde Consulting SARL Bénin, Abomey-Calavi, Arconville

Missions : Evaluation de la qualité du code, participation à la revue de code et à l'amélioration
continue des processus de développement, intégration de tests automatisés pour assurer la qualité
du code et réduire les erreurs

Stagiaire, Développeur Web : D'août 2022 à septembre 2022

Lieu : Foortina Prime - Parakou
Missions : Conception et déploiement d'Applications Web avec Vue.js/Nuxt.js, Création d’APIs REST

avec Express.js + MongoDB

Compétences

e Programmation web : HTML, CSS, Javascript/Typescript, PHP

e Langages de programmation C, C++, python, Java

e Framework : Laravel, Express.js, Vue.js/Nuxt.js, Flutter, Flask, Django, Angular

e Data Science : Collecte, Nettoyage, Analyse des données, Machine Leaning avec Scikit-Learn
e CMS: Wordpress

e Base de données : MySQL, MongoDB, Firestore, Oracle, PostgreSQL, MS SQL Server

e Cloud : AWS, Digital Ocean, Heroku, Docker, Vercel

e Conception et Design : Figma, Adobe XD

e Bonne maîtrise de la méthodologie de gestion d’un projet informatique

Je certifie sincères les informations que voici.

"""

# schema = {
#     "properties": {
#         "nom": {"type": "string"},
#         "email": {"type": "string"},
#         "experiences": {"type": "array", "items": {"type": "string"}},
#         "diplomes": {"type": "array", "items": {"type": "string"}}
#     },
#     "required": ["nom", "email"]
# }
# api_key = "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"


# # Initialisation du modèle (par exemple, gpt-3.5-turbo)
# llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", api_key=api_key)

# # Création de la chaîne d'extraction
# chain = create_extraction_chain(schema, llm)

# # Exécution de la chaîne sur le texte du CV
# result = chain.run(cv_text)

# # Résultat
# nom = result[0]["nom"]
# email = result[0]["email"]
# experiences = result[0]["experiences"]
# diplomes = result[0]["diplomes"]

# print(f"Nom : {nom}")
# print(f"E-mail : {email}")
# print(f"Expériences : {experiences}")
# print(f"Diplômes : {diplomes}")

# Texte du CV (remplacez par votre variable cv_text)
# cv_text = "John Doe\njohn.doe@email.com\nExpérience : Ingénieur logiciel chez XYZ\nDiplômes : Master en informatique"

schema = {
    "properties": {
        "nom": {"type": "string"},
        "email": {"type": "string"},
        "experiences": {"type": "array", "items": {"type": "string"}},
        "diplomes": {"type": "array", "items": {"type": "string"}},
        "competences": {"type": "array", "items": {"type": "string"}},
        "outils": {"type": "array", "items": {"type": "string"}},
        "langues": {"type": "array", "items": {"type": "string"}},
        "contact": {"type": "array", "items": {"type": "string"}},
        "telephone": {"type": "string"},
    },
    "required": ["nom", "email"]
}


api_key = "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"


# # Initialisation du modèle (par exemple, gpt-3.5-turbo)
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", api_key=api_key)

# Création de la chaîne d'extraction
chain = create_extraction_chain(schema, llm)

# Exécution de la chaîne sur le texte du CV
result = chain.run(cv_text)

# Résultat
nom = result[0]["nom"]
email = result[0]["email"]
experiences = result[0]["experiences"]
diplomes = result[0]["diplomes"]
competences = result[0]["competences"]
outils = result[0].get("outils", [])
langues = result[0]["langues"]
telephone = result[0]["telephone"]
# contact = result[0]["contacts"]

print(f"Nom : {nom}")
print(f"E-mail : {email}")
print(f"Expériences : {experiences}")
print(f"Diplômes : {diplomes}")
print(f"Compétences : {competences}")
print(f"Outils : {outils}")
print(f"Langues : {langues}")
print(f"Telephone : {langues}")
# print(f"Contacts : {contact}")
