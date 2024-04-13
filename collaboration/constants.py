from enum import Enum


class StatutInvitation(Enum):
    EN_ATTENTE = "En attente"
    ACCEPTEE = "Acceptée"
    EXPIREE = "Expirée"
    


class Role(Enum):
    LECTURE = "Lecture"
    ECRITURE = "Ecriture"
