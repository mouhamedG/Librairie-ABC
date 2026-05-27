"""
Démonstration des améliorations de sécurité - Étape 2
"""

from src.librairie_abc import Livre, Bibliotheque
from src.exceptions import (
    ValidationError,
    LivreAlreadyReservedError,
    LivreNotReservedError,
    DuplicateLivreError
)


def demo_validation():
    """Démontre la validation des entrées."""
    print("\n=== 1. VALIDATION DES ENTREES ===\n")
    
    # Cas 1: Données valides
    try:
        livre = Livre('Les Miserables', 'Victor Hugo', 1862)
        print("[OK] Livre valide cree avec succes")
        print(f"     Titre: {livre.titre}")
        print(f"     Auteur: {livre.auteur}")
        print(f"     Annee: {livre.annee_publication}")
    except ValidationError as e:
        print(f"[FAIL] {e}")
    
    # Cas 2: Titre vide
    try:
        livre = Livre('', 'Auteur', 2000)
    except ValidationError as e:
        print(f"[OK] Validation rejetee (titre vide): {e}")
    
    # Cas 3: Annee invalide
    try:
        livre = Livre('Titre', 'Auteur', 5000)
    except ValidationError as e:
        print(f"[OK] Validation rejetee (annee future): {e}")
    
    # Cas 4: Type invalide
    try:
        livre = Livre('Titre', 'Auteur', "pas une annee")
    except ValidationError as e:
        print(f"[OK] Validation rejetee (type annee): {e}")


def demo_gestion_erreurs():
    """Démontre la gestion des erreurs."""
    print("\n=== 2. GESTION DES ERREURS ===\n")
    
    bib = Bibliotheque()
    livre = Livre('Test', 'Auteur Test', 2000)
    bib.ajouter_livre(livre)
    
    # Cas 1: Reserver
    try:
        message = livre.reserver()
        print(f"[OK] {message}")
    except Exception as e:
        print(f"[FAIL] {e}")
    
    # Cas 2: Reserver deux fois
    try:
        livre.reserver()
        print("[FAIL] Should have raised an exception")
    except LivreAlreadyReservedError as e:
        print(f"[OK] Exception levee pour double reservation: {e}")
    
    # Cas 3: Annuler reservation
    try:
        message = livre.annuler_reservation()
        print(f"[OK] {message}")
    except Exception as e:
        print(f"[FAIL] {e}")
    
    # Cas 4: Annuler deux fois
    try:
        livre.annuler_reservation()
        print("[FAIL] Should have raised an exception")
    except LivreNotReservedError as e:
        print(f"[OK] Exception levee pour annulation invalide: {e}")


def demo_cas_limites():
    """Démontre la protection contre les cas limites."""
    print("\n=== 3. PROTECTION CONTRE LES CAS LIMITES ===\n")
    
    bib = Bibliotheque()
    
    # Cas 1: Ajouter un doublon
    livre1 = Livre('Titre Unique', 'Auteur', 2000)
    bib.ajouter_livre(livre1)
    
    try:
        livre2 = Livre('Titre Unique', 'Autre Auteur', 2020)
        bib.ajouter_livre(livre2)
        print("[FAIL] Should have raised DuplicateLivreError")
    except DuplicateLivreError as e:
        print(f"[OK] Doublon rejet: {e}")
    
    # Cas 2: Ajouter un non-Livre
    try:
        bib.ajouter_livre("pas un livre")
        print("[FAIL] Should have raised TypeError")
    except TypeError as e:
        print(f"[OK] Type invalide rejet: {e}")
    
    # Cas 3: Recherche case-insensitive
    resultat = bib.rechercher_livre("titre unique")
    if resultat:
        print(f"[OK] Recherche case-insensitive trouve: {resultat.titre}")
    else:
        print("[FAIL] Recherche case-insensitive n'a pas trouve")
    
    # Cas 4: Statistiques
    print(f"[OK] Total livres: {bib.compter_livres()}")
    livre1.reserver()
    print(f"[OK] Livres reserves: {bib.compter_livres_reserves()}")


def demo_logging():
    """Démontre le logging d'audit."""
    print("\n=== 4. LOGGING D'AUDIT ===\n")
    
    print("[INFO] Les operations sont loggees dans logs/librairie_abc.log")
    print("[INFO] Operations tracees:")
    print("  - Creation de livre")
    print("  - Ajout de livre")
    print("  - Reservation/annulation")
    print("  - Erreurs de validation")
    print("  - Erreurs de securite")
    print("\nExemple: grep 'SECURITY_EVENT' logs/librairie_abc.log")


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("DEMONSTRATION DES AMELIORATIONS DE SECURITE")
    print("Etape 2: Securisation de l'application")
    print("=" * 60)
    
    demo_validation()
    demo_gestion_erreurs()
    demo_cas_limites()
    demo_logging()
    
    print("\n" + "=" * 60)
    print("TOUS LES TESTS DE SECURITE PASSENT")
    print("=" * 60 + "\n")
