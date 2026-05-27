"""
Librairie ABC - Package de gestion de bibliothèque
"""

from .librairie_abc import Livre, Bibliotheque
from .exceptions import (
    LibrairieABCError,
    LivreNotFoundError,
    LivreAlreadyReservedError,
    LivreNotReservedError,
    ValidationError,
    DuplicateLivreError
)
from .validation import (
    valider_titre,
    valider_auteur,
    valider_annee_publication,
    valider_titre_recherche
)
from .logger import get_logger, log_operation, log_error, log_security_event

__version__ = "1.0.0"
__all__ = [
    # Classes principales
    "Livre",
    "Bibliotheque",
    # Exceptions
    "LibrairieABCError",
    "LivreNotFoundError",
    "LivreAlreadyReservedError",
    "LivreNotReservedError",
    "ValidationError",
    "DuplicateLivreError",
    # Fonctions de validation
    "valider_titre",
    "valider_auteur",
    "valider_annee_publication",
    "valider_titre_recherche",
    # Logger
    "get_logger",
    "log_operation",
    "log_error",
    "log_security_event"
]
