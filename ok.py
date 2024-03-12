import openai
import json

# Clé API OpenAI
api_key = "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"

# Définir le modèle

client = openai.OpenAI(api_key=api_key)

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


chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"""
    ## Extraction d'informations d'un CV

    **Texte du CV:**

    {cv_text}

    **Informations à extraire:**

    - Nom complet
    - Email
    - Expériences
    - Diplômes

    **Format de sortie:**

    - Clé : Valeur

    **Exemple:**

    - Nom complet: John Doe
    - Email: john.doe@example.com

    **Sortie:**

    """,
        }
    ],

    model="gpt-3.5-turbo",
    max_tokens=
    
)

# Extraction des informations
# informations = chat_completion["choices"][0]["text"].split("\n")
choice = chat_completion.choices[0]
# print(choice.message.model_dump())
ok = choice.message.model_dump()
# Écrire dans le fichier JSON
with open("file.json", 'w') as fichier:
    json.dump(choice.message.model_dump(), fichier, indent=4)

# print(ok['content'].split('\n'))
# # Parcourir les informations
for information in ok['content'].split('\n'):
    # Séparer la clé et la valeur
    cle, valeur = information.split(":")

    # Afficher les informations
    print(f"{cle}: {valeur}")
