from enum import Enum


class StatutInvitation(Enum):
    ENVOYE = "Envoyée"
    ACCEPTEE = "Acceptée"
    EXPIREE = "Expirée"
    


class Role(Enum):
    LECTURE = "Lecture"
    ECRITURE = "Ecriture"
