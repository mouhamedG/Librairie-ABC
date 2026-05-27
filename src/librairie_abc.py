"""
Module de gestion de bibliothèque - Librairie ABC
Contient les classes Livre et Bibliotheque pour gérer les livres et les réservations.
Inclut validation des données, gestion d'erreurs et logging de sécurité.
"""

from typing import List, Optional

# Gérer les imports relatifs et absolus
try:
    from .validation import valider_titre, valider_auteur, valider_annee_publication, valider_titre_recherche, ValidationError
    from .exceptions import (
        LivreAlreadyReservedError,
        LivreNotReservedError,
        LivreNotFoundError,
        DuplicateLivreError
    )
    from .logger import log_operation, log_error, log_validation_error, log_security_event
except ImportError:
    # Fallback pour imports directs
    from validation import valider_titre, valider_auteur, valider_annee_publication, valider_titre_recherche, ValidationError
    from exceptions import (
        LivreAlreadyReservedError,
        LivreNotReservedError,
        LivreNotFoundError,
        DuplicateLivreError
    )
    from logger import log_operation, log_error, log_validation_error, log_security_event


class Livre:
    """
    Représente un livre dans la bibliothèque.
    
    Attributes:
        titre (str): Titre du livre (validé, max 500 caractères)
        auteur (str): Nom de l'auteur (validé, max 500 caractères)
        annee_publication (int): Année de publication (validée, 1440-2100)
        reserve (bool): État de réservation du livre
    """
    
    def __init__(self, titre: str, auteur: str, annee_publication: int) -> None:
        """
        Initialise un livre avec validation des données.
        
        Args:
            titre: Titre du livre
            auteur: Nom de l'auteur
            annee_publication: Année de publication
            
        Raises:
            ValidationError: Si une donnée est invalide
        """
        try:
            self.titre = valider_titre(titre)
            self.auteur = valider_auteur(auteur)
            self.annee_publication = valider_annee_publication(annee_publication)
            self.reserve = False
            log_operation('livre_cree', {'titre': self.titre[:50]})  # Limiter la longueur du log
        except ValidationError as e:
            log_validation_error('Livre.__init__', str(e))
            raise

    def reserver(self) -> str:
        """
        Réserve le livre si possible.
        
        Returns:
            Message de confirmation
            
        Raises:
            LivreAlreadyReservedError: Si le livre est déjà réservé
        """
        if self.reserve:
            error_msg = f"{self.titre} est déjà réservé."
            log_security_event('reservation_echouee', {'raison': 'livre_deja_reserve', 'titre': self.titre[:50]})
            raise LivreAlreadyReservedError(self.titre)
        
        self.reserve = True
        log_operation('livre_reserve', {'titre': self.titre[:50]})
        return f"{self.titre} a été réservé."

    def annuler_reservation(self) -> str:
        """
        Annule la réservation du livre si possible.
        
        Returns:
            Message de confirmation
            
        Raises:
            LivreNotReservedError: Si le livre n'est pas réservé
        """
        if not self.reserve:
            error_msg = f"{self.titre} n'est pas réservé."
            log_security_event('annulation_echouee', {'raison': 'livre_non_reserve', 'titre': self.titre[:50]})
            raise LivreNotReservedError(self.titre)
        
        self.reserve = False
        log_operation('reservation_annulee', {'titre': self.titre[:50]})
        return f"La réservation de {self.titre} a été annulée."


class Bibliotheque:
    """
    Gère une collection de livres.
    
    Attributes:
        livres (List[Livre]): Liste des livres de la bibliothèque
    """
    
    def __init__(self) -> None:
        """Initialise une bibliothèque vide."""
        self.livres: List[Livre] = []
        log_operation('bibliotheque_initialisee')

    def ajouter_livre(self, livre: Livre) -> None:
        """
        Ajoute un livre à la bibliothèque.
        
        Args:
            livre: Le livre à ajouter
            
        Raises:
            TypeError: Si l'argument n'est pas une instance de Livre
            DuplicateLivreError: Si un livre avec le même titre existe déjà
        """
        if not isinstance(livre, Livre):
            error_msg = f"Argument doit être une instance de Livre, reçu: {type(livre).__name__}"
            log_error('TYPE_ERROR', error_msg)
            raise TypeError(error_msg)
        
        # Vérifier les doublons
        if self.rechercher_livre(livre.titre):
            error_msg = f"Un livre avec le titre '{livre.titre}' existe déjà"
            log_security_event('ajout_livre_doublon', {'titre': livre.titre[:50]})
            raise DuplicateLivreError(livre.titre)
        
        self.livres.append(livre)
        log_operation('livre_ajoute', {'titre': livre.titre[:50], 'nb_livres_total': len(self.livres)})

    def lister_livres(self) -> List[str]:
        """
        Liste tous les titres des livres.
        
        Returns:
            Liste des titres des livres (peut être vide)
        """
        titres = [livre.titre for livre in self.livres]
        log_operation('livres_listes', {'nombre': len(titres)})
        return titres

    def rechercher_livre(self, titre: str) -> Optional[Livre]:
        """
        Recherche un livre par titre (case-insensitive).
        
        Args:
            titre: Le titre à rechercher
            
        Returns:
            L'objet Livre si trouvé, None sinon
            
        Raises:
            ValidationError: Si le titre est invalide
        """
        try:
            titre_clean = valider_titre_recherche(titre)
        except ValidationError as e:
            log_validation_error('recherche_livre', str(e))
            raise
        
        # Si la recherche est vide, retourner None
        if not titre_clean:
            return None
        
        for livre in self.livres:
            if livre.titre.lower() == titre_clean.lower():
                log_operation('livre_trouve', {'titre': livre.titre[:50]})
                return livre
        
        log_operation('livre_non_trouve', {'titre': titre_clean[:50]})
        return None
    
    def obtenir_livre_par_titre(self, titre: str) -> Livre:
        """
        Obtient un livre par titre ou lève une exception.
        
        Args:
            titre: Le titre du livre
            
        Returns:
            L'objet Livre
            
        Raises:
            ValidationError: Si le titre est invalide
            LivreNotFoundError: Si le livre n'existe pas
        """
        try:
            titre_clean = valider_titre_recherche(titre)
        except ValidationError as e:
            log_validation_error('obtenir_livre', str(e))
            raise
        
        livre = self.rechercher_livre(titre_clean)
        if not livre:
            log_error('LIVRE_NOT_FOUND', f"Livre non trouvé", {'titre': titre_clean[:50]})
            raise LivreNotFoundError(titre_clean)
        
        return livre
    
    def compter_livres(self) -> int:
        """
        Retourne le nombre total de livres.
        
        Returns:
            Nombre de livres dans la bibliothèque
        """
        count = len(self.livres)
        log_operation('compter_livres', {'nombre': count})
        return count
    
    def compter_livres_reserves(self) -> int:
        """
        Retourne le nombre de livres réservés.
        
        Returns:
            Nombre de livres réservés
        """
        count = sum(1 for livre in self.livres if livre.reserve)
        log_operation('compter_livres_reserves', {'nombre': count})
        return count
