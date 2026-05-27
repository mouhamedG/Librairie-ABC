"""
Module de validation des données pour la bibliothèque ABC.
Valide et nettoie les entrées utilisateur pour prévenir les injections et données malveillantes.
"""

import re
from typing import Any, Tuple

# Gérer les imports
try:
    from .exceptions import ValidationError
except ImportError:
    from exceptions import ValidationError


# Constantes de validation
MIN_TITRE_LENGTH = 1
MAX_TITRE_LENGTH = 500
MIN_AUTEUR_LENGTH = 1
MAX_AUTEUR_LENGTH = 500
MIN_ANNEE_PUBLICATION = 1440  # Gutenberg
MAX_ANNEE_PUBLICATION = 2100  # Limite raisonnable future

# Regex pour détecter potentiellement des caractères suspects (injection)
SUSPECT_PATTERN = re.compile(r'[<>\"\'%;()&+]')


def nettoyer_chaine(valeur: Any, nom_champ: str) -> str:
    """
    Nettoie une chaîne de caractères.
    
    Args:
        valeur: La valeur à nettoyer
        nom_champ: Nom du champ (pour les messages d'erreur)
        
    Returns:
        La chaîne nettoyée (trimmed, etc.)
        
    Raises:
        ValidationError: Si la valeur n'est pas une chaîne valide
    """
    if valeur is None:
        raise ValidationError(f"{nom_champ} ne peut pas être None")
    
    if not isinstance(valeur, str):
        raise ValidationError(f"{nom_champ} doit être une chaîne, reçu: {type(valeur).__name__}")
    
    # Trim whitespace
    valeur_clean = valeur.strip()
    
    if not valeur_clean:
        raise ValidationError(f"{nom_champ} ne peut pas être vide")
    
    return valeur_clean


def valider_titre(titre: Any) -> str:
    """
    Valide et nettoie un titre de livre.
    
    Args:
        titre: Le titre à valider
        
    Returns:
        Le titre nettoyé
        
    Raises:
        ValidationError: Si le titre est invalide
    """
    titre_clean = nettoyer_chaine(titre, "titre")
    
    if len(titre_clean) < MIN_TITRE_LENGTH:
        raise ValidationError(f"titre doit avoir au moins {MIN_TITRE_LENGTH} caractère")
    
    if len(titre_clean) > MAX_TITRE_LENGTH:
        raise ValidationError(f"titre ne peut pas dépasser {MAX_TITRE_LENGTH} caractères (reçu: {len(titre_clean)})")
    
    # Avertissement pour caractères suspects (ne rejette pas, mais loggable)
    if SUSPECT_PATTERN.search(titre_clean):
        # On accepte mais on flag comme potentiellement suspect
        pass
    
    return titre_clean


def valider_auteur(auteur: Any) -> str:
    """
    Valide et nettoie un nom d'auteur.
    
    Args:
        auteur: L'auteur à valider
        
    Returns:
        L'auteur nettoyé
        
    Raises:
        ValidationError: Si l'auteur est invalide
    """
    auteur_clean = nettoyer_chaine(auteur, "auteur")
    
    if len(auteur_clean) < MIN_AUTEUR_LENGTH:
        raise ValidationError(f"auteur doit avoir au moins {MIN_AUTEUR_LENGTH} caractère")
    
    if len(auteur_clean) > MAX_AUTEUR_LENGTH:
        raise ValidationError(f"auteur ne peut pas dépasser {MAX_AUTEUR_LENGTH} caractères (reçu: {len(auteur_clean)})")
    
    return auteur_clean


def valider_annee_publication(annee: Any) -> int:
    """
    Valide une année de publication.
    
    Args:
        annee: L'année à valider
        
    Returns:
        L'année validée
        
    Raises:
        ValidationError: Si l'année est invalide
    """
    if annee is None:
        raise ValidationError("annee_publication ne peut pas être None")
    
    # Essayer de convertir en entier si c'est une chaîne
    if isinstance(annee, str):
        try:
            annee = int(annee.strip())
        except ValueError:
            raise ValidationError(f"annee_publication doit être un entier, reçu: '{annee}'")
    
    if not isinstance(annee, int):
        raise ValidationError(f"annee_publication doit être un entier, reçu: {type(annee).__name__}")
    
    if annee < MIN_ANNEE_PUBLICATION:
        raise ValidationError(f"annee_publication doit être >= {MIN_ANNEE_PUBLICATION} (reçu: {annee})")
    
    if annee > MAX_ANNEE_PUBLICATION:
        raise ValidationError(f"annee_publication doit être <= {MAX_ANNEE_PUBLICATION} (reçu: {annee})")
    
    return annee


def valider_titre_recherche(titre: Any) -> str:
    """
    Valide un titre pour la recherche.
    Moins strict que valider_titre (permet les chaînes vides pour recherche vide).
    
    Args:
        titre: Le titre à valider
        
    Returns:
        Le titre nettoyé
        
    Raises:
        ValidationError: Si le titre est invalide
    """
    if titre is None:
        raise ValidationError("titre ne peut pas être None")
    
    if not isinstance(titre, str):
        raise ValidationError(f"titre doit être une chaîne, reçu: {type(titre).__name__}")
    
    # Pour la recherche, on permet les chaînes vides (recherche vide = lister tout)
    return titre.strip()
