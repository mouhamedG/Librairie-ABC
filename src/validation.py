"""
Module de validation des données pour la bibliothèque ABC.

Valide et nettoie les entrées utilisateur pour prévenir les injections
et les données malveillantes.
"""

import re
from typing import Any

try:
    from .exceptions import ValidationError
except ImportError:
    from exceptions import ValidationError


MIN_TITRE_LENGTH = 1
MAX_TITRE_LENGTH = 500
MIN_AUTEUR_LENGTH = 1
MAX_AUTEUR_LENGTH = 500
MIN_ANNEE_PUBLICATION = 1440
MAX_ANNEE_PUBLICATION = 2100

SUSPECT_PATTERN = re.compile(r"[<>\"'%;()&+]")


def nettoyer_chaine(valeur: Any, nom_champ: str) -> str:
    """
    Nettoie une chaîne de caractères.

    Args:
        valeur: Valeur à nettoyer.
        nom_champ: Nom du champ.

    Returns:
        Chaîne nettoyée.

    Raises:
        ValidationError: si la valeur est invalide.
    """
    if valeur is None:
        raise ValidationError(f"{nom_champ} ne peut pas être None")

    if not isinstance(valeur, str):
        raise ValidationError(
            f"{nom_champ} doit être une chaîne, "
            f"reçu: {type(valeur).__name__}"
        )

    valeur_clean = valeur.strip()

    if not valeur_clean:
        raise ValidationError(f"{nom_champ} ne peut pas être vide")

    return valeur_clean


def valider_titre(titre: Any) -> str:
    """
    Valide et nettoie un titre de livre.

    Args:
        titre: Titre à valider.

    Returns:
        Titre nettoyé.

    Raises:
        ValidationError: si le titre est invalide.
    """
    titre_clean = nettoyer_chaine(titre, "titre")

    if len(titre_clean) < MIN_TITRE_LENGTH:
        raise ValidationError(
            f"titre doit avoir au moins {MIN_TITRE_LENGTH} caractère"
        )

    if len(titre_clean) > MAX_TITRE_LENGTH:
        raise ValidationError(
            f"titre ne peut pas dépasser {MAX_TITRE_LENGTH} caractères "
            f"(reçu: {len(titre_clean)})"
        )

    return titre_clean


def valider_auteur(auteur: Any) -> str:
    """
    Valide et nettoie un nom d'auteur.

    Args:
        auteur: Auteur à valider.

    Returns:
        Auteur nettoyé.

    Raises:
        ValidationError: si l'auteur est invalide.
    """
    auteur_clean = nettoyer_chaine(auteur, "auteur")

    if len(auteur_clean) < MIN_AUTEUR_LENGTH:
        raise ValidationError(
            f"auteur doit avoir au moins {MIN_AUTEUR_LENGTH} caractère"
        )

    if len(auteur_clean) > MAX_AUTEUR_LENGTH:
        raise ValidationError(
            f"auteur ne peut pas dépasser {MAX_AUTEUR_LENGTH} caractères "
            f"(reçu: {len(auteur_clean)})"
        )

    return auteur_clean


def valider_annee_publication(annee: Any) -> int:
    """
    Valide une année de publication.

    Args:
        annee: Année à valider.

    Returns:
        Année validée.

    Raises:
        ValidationError: si l'année est invalide.
    """
    if annee is None:
        raise ValidationError("annee_publication ne peut pas être None")

    if isinstance(annee, str):
        try:
            annee = int(annee.strip())
        except ValueError as error:
            raise ValidationError(
                f"annee_publication doit être un entier, reçu: '{annee}'"
            ) from error

    if not isinstance(annee, int):
        raise ValidationError(
            f"annee_publication doit être un entier, "
            f"reçu: {type(annee).__name__}"
        )

    if annee < MIN_ANNEE_PUBLICATION:
        raise ValidationError(
            f"annee_publication doit être >= {MIN_ANNEE_PUBLICATION} "
            f"(reçu: {annee})"
        )

    if annee > MAX_ANNEE_PUBLICATION:
        raise ValidationError(
            f"annee_publication doit être <= {MAX_ANNEE_PUBLICATION} "
            f"(reçu: {annee})"
        )

    return annee


def valider_titre_recherche(titre: Any) -> str:
    """
    Valide un titre pour la recherche.

    Args:
        titre: Titre à valider.

    Returns:
        Titre nettoyé.

    Raises:
        ValidationError: si le titre est invalide.
    """
    if titre is None:
        raise ValidationError("titre ne peut pas être None")

    if not isinstance(titre, str):
        raise ValidationError(
            f"titre doit être une chaîne, reçu: {type(titre).__name__}"
        )

    return titre.strip()
    

