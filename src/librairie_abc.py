"""
Module de gestion de bibliothèque - Librairie ABC.

Contient les classes Livre et Bibliotheque pour gérer les livres
et les réservations.
Inclut validation des données, gestion d'erreurs
et logging de sécurité.
"""

try:
    from .validation import (
        valider_titre,
        valider_auteur,
        valider_annee_publication,
        valider_titre_recherche,
        ValidationError,
    )
    from .exceptions import (
        LivreAlreadyReservedError,
        LivreNotReservedError,
        LivreNotFoundError,
        DuplicateLivreError,
    )
    from .logger import (
        log_operation,
        log_error,
        log_validation_error,
        log_security_event,
    )
except ImportError:
    from validation import (
        valider_titre,
        valider_auteur,
        valider_annee_publication,
        valider_titre_recherche,
        ValidationError,
    )
    from exceptions import (
        LivreAlreadyReservedError,
        LivreNotReservedError,
        LivreNotFoundError,
        DuplicateLivreError,
    )
    from logger import (
        log_operation,
        log_error,
        log_validation_error,
        log_security_event,
    )


class Livre:
    """Représente un livre dans la bibliothèque."""

    def __init__(
        self,
        titre: str,
        auteur: str,
        annee_publication: int,
    ) -> None:
        """
        Initialise un livre avec validation des données.

        Args:
            titre: Titre du livre.
            auteur: Auteur du livre.
            annee_publication: Année de publication.

        Raises:
            ValidationError:
                Si les données du livre sont invalides.
        """
        try:
            self.titre = valider_titre(titre)
            self.auteur = valider_auteur(auteur)
            self.annee_publication = (
                valider_annee_publication(
                    annee_publication
                )
            )
            self.reserve = False

            log_operation(
                "livre_cree",
                {"titre": self.titre[:50]},
            )

        except ValidationError as error:
            log_validation_error(
                "Livre.__init__",
                str(error),
            )
            raise

    def reserver(self) -> str:
        """
        Réserve le livre si possible.

        Returns:
            Message de confirmation.

        Raises:
            LivreAlreadyReservedError:
                Si le livre est déjà réservé.
        """
        if self.reserve:
            log_security_event(
                "reservation_echouee",
                {
                    "raison": "livre_deja_reserve",
                    "titre": self.titre[:50],
                },
            )

            raise LivreAlreadyReservedError(
                self.titre
            )

        self.reserve = True

        log_operation(
            "livre_reserve",
            {"titre": self.titre[:50]},
        )

        return (
            f"{self.titre} a été réservé."
        )

    def annuler_reservation(self) -> str:
        """
        Annule la réservation du livre.

        Returns:
            Message de confirmation.

        Raises:
            LivreNotReservedError:
                Si le livre n'est pas réservé.
        """
        if not self.reserve:
            log_security_event(
                "annulation_echouee",
                {
                    "raison": "livre_non_reserve",
                    "titre": self.titre[:50],
                },
            )

            raise LivreNotReservedError(
                self.titre
            )

        self.reserve = False

        log_operation(
            "reservation_annulee",
            {"titre": self.titre[:50]},
        )

        return (
            f"La réservation de "
            f"{self.titre} a été annulée."
        )


class Bibliotheque:
    """Gère une collection de livres."""

    def __init__(self) -> None:
        """Initialise une bibliothèque vide."""
        self.livres: list[Livre] = []

        log_operation(
            "bibliotheque_initialisee"
        )

    def ajouter_livre(
        self,
        livre: Livre,
    ) -> None:
        """
        Ajoute un livre à la bibliothèque.

        Args:
            livre: Livre à ajouter.

        Raises:
            TypeError:
                Si l'objet n'est pas un Livre.
            DuplicateLivreError:
                Si le livre existe déjà.
            ValidationError:
                Si le titre est invalide.
        """
        if not isinstance(
            livre,
            Livre,
        ):
            error_msg = (
                "Argument doit être "
                "une instance de Livre, "
                f"reçu: "
                f"{type(livre).__name__}"
            )

            log_error(
                "TYPE_ERROR",
                error_msg,
            )

            raise TypeError(error_msg)

        if self.rechercher_livre(
            livre.titre
        ):
            log_security_event(
                "ajout_livre_doublon",
                {
                    "titre":
                    livre.titre[:50]
                },
            )

            raise DuplicateLivreError(
                livre.titre
            )

        self.livres.append(livre)

        log_operation(
            "livre_ajoute",
            {
                "titre":
                livre.titre[:50],
                "nb_livres_total":
                len(self.livres),
            },
        )

    def lister_livres(
        self,
    ) -> list[str]:
        """
        Liste les titres des livres.

        Returns:
            Liste des titres.
        """
        titres = [
            livre.titre
            for livre in self.livres
        ]

        log_operation(
            "livres_listes",
            {"nombre": len(titres)},
        )

        return titres

    def rechercher_livre(
        self,
        titre: str,
    ) -> Livre | None:
        """
        Recherche un livre par titre.

        Args:
            titre: Titre recherché.

        Returns:
            Livre trouvé ou None.

        Raises:
            ValidationError:
                Si le titre est invalide.
        """
        try:
            titre_clean = (
                valider_titre_recherche(
                    titre
                )
            )

        except ValidationError as error:
            log_validation_error(
                "recherche_livre",
                str(error),
            )
            raise

        if not titre_clean:
            return None

        for livre in self.livres:
            if (
                livre.titre.lower()
                == titre_clean.lower()
            ):
                log_operation(
                    "livre_trouve",
                    {
                        "titre":
                        livre.titre[:50]
                    },
                )

                return livre

        log_operation(
            "livre_non_trouve",
            {
                "titre":
                titre_clean[:50]
            },
        )

        return None

    def obtenir_livre_par_titre(
        self,
        titre: str,
    ) -> Livre:
        """
        Retourne un livre à partir de son titre.

        Args:
            titre: Titre recherché.

        Returns:
            Livre trouvé.

        Raises:
            ValidationError:
                Si le titre est invalide.
            LivreNotFoundError:
                Si le livre n'existe pas.
        """
        try:
            titre_clean = (
                valider_titre_recherche(
                    titre
                )
            )

        except ValidationError as error:
            log_validation_error(
                "obtenir_livre",
                str(error),
            )
            raise

        livre = self.rechercher_livre(
            titre_clean
        )

        if not livre:
            log_error(
                "LIVRE_NOT_FOUND",
                "Livre non trouvé",
                {
                    "titre":
                    titre_clean[:50]
                },
            )

            raise LivreNotFoundError(
                titre_clean
            )

        return livre

    def compter_livres(
        self,
    ) -> int:
        """
        Retourne le nombre total de livres.

        Returns:
            Nombre de livres.
        """
        count = len(self.livres)

        log_operation(
            "compter_livres",
            {"nombre": count},
        )

        return count

    def compter_livres_reserves(
        self,
    ) -> int:
        """
        Retourne le nombre de livres réservés.

        Returns:
            Nombre de livres réservés.
        """
        count = sum(
            1
            for livre in self.livres
            if livre.reserve
        )

        log_operation(
            "compter_livres_reserves",
            {"nombre": count},
        )

        return count
        
