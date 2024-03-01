# import spacy
# import re
# import sys
# import fitz
# fname = './uploads/cv16.pdf'
# doc = fitz.open(fname)
# text = " "
# for page in doc:
#     text = text + str(page.get_text())
# print(text)
import spacy
nlp = spacy.load("fr_core_news_lg")


# def recuperer_premiere_email(chaine):
#     # Modèle d'expression régulière pour trouver une adresse e-mail
#     modele_regex = r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$'

#     # Utilisation de la fonction search() de re pour trouver la première adresse e-mail
#     correspondance = re.search(modele_regex, "tanguyﬁchot@gmail.com")

#     if correspondance:
#         return correspondance.group()
#     else:
#         return None


# # # Exemple d'utilisation
# # premiere_adresse_email = recuperer_premiere_email(text)

# # # Afficher la première adresse e-mail trouvée
# # if premiere_adresse_email:
# #     print(f"Première adresse e-mail trouvée : {premiere_adresse_email}")
# # else:
# #     print("Aucune adresse e-mail trouvée dans la chaîne.")
