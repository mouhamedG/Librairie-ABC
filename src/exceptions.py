"""
Exceptions personnalisées pour la bibliothèque ABC.
"""


class LibrairieABCError(Exception):
    """Exception de base pour la bibliothèque ABC."""
    pass


class LivreNotFoundError(LibrairieABCError):
    """Exception levée quand un livre n'est pas trouvé."""
    
    def __init__(self, titre: str):
        self.titre = titre
        super().__init__(f"Livre non trouvé: {titre}")


class LivreAlreadyReservedError(LibrairieABCError):
    """Exception levée quand on essaie de réserver un livre déjà réservé."""
    
    def __init__(self, titre: str):
        self.titre = titre
        super().__init__(f"Livre déjà réservé: {titre}")


class LivreNotReservedError(LibrairieABCError):
    """Exception levée quand on essaie d'annuler la réservation d'un livre non réservé."""
    
    def __init__(self, titre: str):
        self.titre = titre
        super().__init__(f"Livre non réservé: {titre}")


class ValidationError(LibrairieABCError):
    """Exception levée lors d'une erreur de validation."""
    pass


class DuplicateLivreError(LibrairieABCError):
    """Exception levée quand on essaie d'ajouter un livre en doublon."""
    
    def __init__(self, titre: str):
        self.titre = titre
        super().__init__(f"Livre en doublon: {titre}")
