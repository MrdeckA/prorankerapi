import re


def is_valid_email(chaine):
    # Modèle d'expression régulière pour vérifier une adresse e-mail
    modele_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # Utilisation de la fonction match() de re pour vérifier la correspondance
    correspondance = re.match(modele_regex, chaine)

    # Si correspondance est None, la chaîne n'est pas une adresse e-mail
    return correspondance is not None


def recuperer_premiere_email(chaine):
    # Modèle d'expression régulière pour trouver une adresse e-mail
    modele_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # Utilisation de la fonction search() de re pour trouver la première adresse e-mail
    correspondance = re.search(modele_regex, chaine)

    if correspondance:
        return correspondance.group()
    else:
        return None
