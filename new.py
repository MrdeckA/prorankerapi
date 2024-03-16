import re 
from unidecode import unidecode
def normaliser_chaine(chaine):

    # Convertir en minuscules
    chaine = chaine.lower()

    # Supprimer les chiffres et les versions
    chaine = re.sub(r'\d+(\.\d+)?', '', chaine)

    # Remplacer les caractères accentués par leur forme sans accent
    chaine = unidecode(chaine)

    # Supprimer les apostrophes et les '/' et les espaces
    # Supprimer les traits d'union ou les points
    chaine = chaine.replace("'", "").replace(
        "/", "").replace(" ", "").replace("-", "").replace(".", "").replace(",", "")

    return chaine

competences =[
                    "Microsoft Word",
                    "Excel",
                    "PowerPoint",
                    "Access",
                    "Adobe Photoshop",
                    "Illustrator"
                ]
for ch in ["cisco", "google", "amazon", "Blockchain developper", "facebook"]:
    for ok in competences:
        if normaliser_chaine(ch) in normaliser_chaine(ok) :
            print(f"{ch} => {ok} => {normaliser_chaine(ch) in normaliser_chaine(ok)}")
