"""
Tests de sécurité pour la bibliothèque ABC.
Teste la validation des entrées, gestion des erreurs, cas limites, et protection contre injections.
"""

import unittest
import sys
from pathlib import Path

# Ajouter src au chemin Python
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from librairie_abc import Livre, Bibliotheque
from validation import (
    valider_titre,
    valider_auteur,
    valider_annee_publication,
    valider_titre_recherche,
    ValidationError,
    MAX_TITRE_LENGTH,
    MAX_AUTEUR_LENGTH,
    MIN_ANNEE_PUBLICATION,
    MAX_ANNEE_PUBLICATION
)
from exceptions import (
    LivreAlreadyReservedError,
    LivreNotReservedError,
    LivreNotFoundError,
    DuplicateLivreError
)


class TestValidationTitre(unittest.TestCase):
    """Tests pour validation de titre."""
    
    def test_titre_valide(self):
        """Un titre valide doit être accepté."""
        resultat = valider_titre("Le Petit Prince")
        self.assertEqual(resultat, "Le Petit Prince")
    
    def test_titre_avec_espaces(self):
        """Les espaces au début/fin doivent être trim."""
        resultat = valider_titre("   Le Petit Prince   ")
        self.assertEqual(resultat, "Le Petit Prince")
    
    def test_titre_none(self):
        """None doit lever une exception."""
        with self.assertRaises(ValidationError) as ctx:
            valider_titre(None)
        self.assertIn("None", str(ctx.exception))
    
    def test_titre_vide(self):
        """Chaîne vide doit lever une exception."""
        with self.assertRaises(ValidationError) as ctx:
            valider_titre("")
        self.assertIn("vide", str(ctx.exception))
    
    def test_titre_espaces_uniquement(self):
        """Chaîne avec espaces uniquement doit lever une exception."""
        with self.assertRaises(ValidationError) as ctx:
            valider_titre("    ")
        self.assertIn("vide", str(ctx.exception))
    
    def test_titre_pas_une_chaine(self):
        """Un entier au lieu de chaîne doit lever une exception."""
        with self.assertRaises(ValidationError) as ctx:
            valider_titre(12345)
        self.assertIn("chaîne", str(ctx.exception))
    
    def test_titre_trop_long(self):
        """Un titre dépassant MAX_TITRE_LENGTH doit être rejeté."""
        titre_long = "A" * (MAX_TITRE_LENGTH + 1)
        with self.assertRaises(ValidationError) as ctx:
            valider_titre(titre_long)
        self.assertIn("dépasser", str(ctx.exception))
    
    def test_titre_avec_caracteres_speciaux(self):
        """Les caractères spéciaux doivent être acceptés (pas rejetés)."""
        # Note: valider_titre accepte mais loggue les caractères suspects
        resultat = valider_titre("L'Avare de Molière")
        self.assertEqual(resultat, "L'Avare de Molière")
    
    def test_titre_avec_injection_potential(self):
        """Les caractères potentiels d'injection doivent être acceptés (auditable)."""
        # Note: On accepte mais loggue. Pas de rejet strict pour permettre les titres légitimes
        resultat = valider_titre("Le code <secret>")
        self.assertEqual(resultat, "Le code <secret>")


class TestValidationAuteur(unittest.TestCase):
    """Tests pour validation d'auteur."""
    
    def test_auteur_valide(self):
        """Un auteur valide doit être accepté."""
        resultat = valider_auteur("Antoine de Saint-Exupéry")
        self.assertEqual(resultat, "Antoine de Saint-Exupéry")
    
    def test_auteur_none(self):
        """None doit lever une exception."""
        with self.assertRaises(ValidationError):
            valider_auteur(None)
    
    def test_auteur_vide(self):
        """Chaîne vide doit lever une exception."""
        with self.assertRaises(ValidationError):
            valider_auteur("")
    
    def test_auteur_pas_une_chaine(self):
        """Pas une chaîne doit lever une exception."""
        with self.assertRaises(ValidationError):
            valider_auteur({"nom": "Alexandre Dumas"})
    
    def test_auteur_trop_long(self):
        """Un auteur trop long doit être rejeté."""
        auteur_long = "A" * (MAX_AUTEUR_LENGTH + 1)
        with self.assertRaises(ValidationError):
            valider_auteur(auteur_long)


class TestValidationAnnee(unittest.TestCase):
    """Tests pour validation d'année de publication."""
    
    def test_annee_valide(self):
        """Une année valide doit être acceptée."""
        resultat = valider_annee_publication(1943)
        self.assertEqual(resultat, 1943)
    
    def test_annee_depuis_chaine(self):
        """Une année en chaîne doit être convertie."""
        resultat = valider_annee_publication("1943")
        self.assertEqual(resultat, 1943)
    
    def test_annee_none(self):
        """None doit lever une exception."""
        with self.assertRaises(ValidationError):
            valider_annee_publication(None)
    
    def test_annee_pas_entier(self):
        """Un float au lieu d'entier doit lever une exception."""
        with self.assertRaises(ValidationError):
            valider_annee_publication(1943.5)
    
    def test_annee_chaine_invalide(self):
        """Une chaîne non-numérique doit lever une exception."""
        with self.assertRaises(ValidationError):
            valider_annee_publication("abc")
    
    def test_annee_trop_ancienne(self):
        """Une année < MIN_ANNEE_PUBLICATION doit être rejetée."""
        with self.assertRaises(ValidationError) as ctx:
            valider_annee_publication(500)
        self.assertIn(str(MIN_ANNEE_PUBLICATION), str(ctx.exception))
    
    def test_annee_trop_future(self):
        """Une année > MAX_ANNEE_PUBLICATION doit être rejetée."""
        with self.assertRaises(ValidationError) as ctx:
            valider_annee_publication(3000)
        self.assertIn(str(MAX_ANNEE_PUBLICATION), str(ctx.exception))
    
    def test_annee_limite_min(self):
        """MIN_ANNEE_PUBLICATION doit être acceptée."""
        resultat = valider_annee_publication(MIN_ANNEE_PUBLICATION)
        self.assertEqual(resultat, MIN_ANNEE_PUBLICATION)
    
    def test_annee_limite_max(self):
        """MAX_ANNEE_PUBLICATION doit être acceptée."""
        resultat = valider_annee_publication(MAX_ANNEE_PUBLICATION)
        self.assertEqual(resultat, MAX_ANNEE_PUBLICATION)


class TestValidationTitreRecherche(unittest.TestCase):
    """Tests pour validation de titre en recherche."""
    
    def test_recherche_titre_valide(self):
        """Un titre de recherche valide doit être accepté."""
        resultat = valider_titre_recherche("Le Petit Prince")
        self.assertEqual(resultat, "Le Petit Prince")
    
    def test_recherche_titre_vide_acceptable(self):
        """En recherche, titre vide doit être accepté (recherche vide)."""
        resultat = valider_titre_recherche("")
        self.assertEqual(resultat, "")
    
    def test_recherche_titre_none(self):
        """None ne doit pas être accepté même en recherche."""
        with self.assertRaises(ValidationError):
            valider_titre_recherche(None)


class TestLivreValidation(unittest.TestCase):
    """Tests pour validation lors de création de Livre."""
    
    def test_livre_valide(self):
        """Créer un livre avec données valides doit fonctionner."""
        livre = Livre("Le Petit Prince", "Antoine de Saint-Exupéry", 1943)
        self.assertEqual(livre.titre, "Le Petit Prince")
        self.assertEqual(livre.auteur, "Antoine de Saint-Exupéry")
        self.assertEqual(livre.annee_publication, 1943)
        self.assertFalse(livre.reserve)
    
    def test_livre_titre_invalide(self):
        """Créer un livre avec titre invalide doit lever ValidationError."""
        with self.assertRaises(ValidationError):
            Livre(None, "Auteur", 2000)
    
    def test_livre_auteur_invalide(self):
        """Créer un livre avec auteur invalide doit lever ValidationError."""
        with self.assertRaises(ValidationError):
            Livre("Titre", "", 2000)
    
    def test_livre_annee_invalide(self):
        """Créer un livre avec année invalide doit lever ValidationError."""
        with self.assertRaises(ValidationError):
            Livre("Titre", "Auteur", 5000)


class TestLivreReservation(unittest.TestCase):
    """Tests pour réservation/annulation avec gestion d'erreurs."""
    
    def setUp(self):
        self.livre = Livre("Test Livre", "Test Auteur", 2000)
    
    def test_reserver_livre_non_reserve(self):
        """Réserver un livre non réservé doit fonctionner."""
        message = self.livre.reserver()
        self.assertIn("réservé", message)
        self.assertTrue(self.livre.reserve)
    
    def test_reserver_livre_deja_reserve(self):
        """Réserver un livre déjà réservé doit lever une exception."""
        self.livre.reserver()
        with self.assertRaises(LivreAlreadyReservedError) as ctx:
            self.livre.reserver()
        self.assertEqual(ctx.exception.titre, "Test Livre")
    
    def test_annuler_reservation_valide(self):
        """Annuler la réservation d'un livre réservé doit fonctionner."""
        self.livre.reserver()
        message = self.livre.annuler_reservation()
        self.assertIn("annulée", message)
        self.assertFalse(self.livre.reserve)
    
    def test_annuler_reservation_non_reserve(self):
        """Annuler la réservation d'un livre non réservé doit lever une exception."""
        with self.assertRaises(LivreNotReservedError) as ctx:
            self.livre.annuler_reservation()
        self.assertEqual(ctx.exception.titre, "Test Livre")


class TestBibliothequeSecurite(unittest.TestCase):
    """Tests de sécurité pour Bibliotheque."""
    
    def setUp(self):
        self.bib = Bibliotheque()
        self.livre = Livre("Test", "Auteur", 2000)
    
    def test_ajouter_livre_valide(self):
        """Ajouter un livre valide doit fonctionner."""
        self.bib.ajouter_livre(self.livre)
        self.assertEqual(self.bib.compter_livres(), 1)
    
    def test_ajouter_pas_un_livre(self):
        """Ajouter un objet qui n'est pas un Livre doit lever TypeError."""
        with self.assertRaises(TypeError):
            self.bib.ajouter_livre("Pas un Livre")
    
    def test_ajouter_doublon(self):
        """Ajouter un doublon doit lever DuplicateLivreError."""
        self.bib.ajouter_livre(self.livre)
        livre_doublon = Livre("Test", "Autre Auteur", 2020)
        with self.assertRaises(DuplicateLivreError) as ctx:
            self.bib.ajouter_livre(livre_doublon)
        self.assertEqual(ctx.exception.titre, "Test")
    
    def test_rechercher_livre_valide(self):
        """Rechercher un livre existant doit le retourner."""
        self.bib.ajouter_livre(self.livre)
        resultat = self.bib.rechercher_livre("Test")
        self.assertEqual(resultat.titre, "Test")
    
    def test_rechercher_livre_inexistant(self):
        """Rechercher un livre inexistant doit retourner None."""
        resultat = self.bib.rechercher_livre("Inexistant")
        self.assertIsNone(resultat)
    
    def test_rechercher_titre_invalide(self):
        """Rechercher avec titre invalide doit lever ValidationError."""
        with self.assertRaises(ValidationError):
            self.bib.rechercher_livre(None)
    
    def test_rechercher_case_insensitive(self):
        """La recherche doit être case-insensitive."""
        self.bib.ajouter_livre(self.livre)
        resultat = self.bib.rechercher_livre("test")
        self.assertEqual(resultat.titre, "Test")
    
    def test_obtenir_livre_par_titre_trouve(self):
        """obtenir_livre_par_titre doit retourner le livre si trouvé."""
        self.bib.ajouter_livre(self.livre)
        resultat = self.bib.obtenir_livre_par_titre("Test")
        self.assertEqual(resultat.titre, "Test")
    
    def test_obtenir_livre_par_titre_pas_trouve(self):
        """obtenir_livre_par_titre doit lever LivreNotFoundError si pas trouvé."""
        with self.assertRaises(LivreNotFoundError) as ctx:
            self.bib.obtenir_livre_par_titre("Inexistant")
        self.assertEqual(ctx.exception.titre, "Inexistant")
    
    def test_compter_livres(self):
        """compter_livres doit retourner le nombre correct."""
        self.assertEqual(self.bib.compter_livres(), 0)
        self.bib.ajouter_livre(self.livre)
        self.assertEqual(self.bib.compter_livres(), 1)
    
    def test_compter_livres_reserves(self):
        """compter_livres_reserves doit compter correctement."""
        self.bib.ajouter_livre(self.livre)
        self.assertEqual(self.bib.compter_livres_reserves(), 0)
        self.livre.reserver()
        self.assertEqual(self.bib.compter_livres_reserves(), 1)
    
    def test_lister_livres_vides(self):
        """Lister une bibliothèque vide doit retourner une liste vide."""
        resultat = self.bib.lister_livres()
        self.assertEqual(resultat, [])
    
    def test_lister_livres_multiples(self):
        """Lister doit retourner tous les titres."""
        livre2 = Livre("Autre Livre", "Auteur2", 2020)
        self.bib.ajouter_livre(self.livre)
        self.bib.ajouter_livre(livre2)
        resultat = self.bib.lister_livres()
        self.assertEqual(len(resultat), 2)
        self.assertIn("Test", resultat)
        self.assertIn("Autre Livre", resultat)


class TestCasLimitesSecurite(unittest.TestCase):
    """Tests des cas limites pour sécurité."""
    
    def test_titre_caracterez_unicode(self):
        """Les caractères unicode doivent être acceptés."""
        livre = Livre("Les Misérables", "Victor Hugo", 1862)
        self.assertEqual(livre.titre, "Les Misérables")
    
    def test_titre_caracteres_speciaux_nombreux(self):
        """Titres avec beaucoup de caractères spéciaux doivent être audités."""
        # Accepté mais auditable via logging
        livre = Livre("Test!@#$%^&*()", "Auteur", 2000)
        self.assertEqual(livre.titre, "Test!@#$%^&*()")
    
    def test_auteur_nom_compose(self):
        """Les noms d'auteur composés doivent être acceptés."""
        livre = Livre("Titre", "Marie-José de Saint-Cyr O'Connor", 2000)
        self.assertEqual(livre.auteur, "Marie-José de Saint-Cyr O'Connor")
    
    def test_operations_multiples_concurrentes_simulation(self):
        """Test de comportement avec opérations répétées."""
        bib = Bibliotheque()
        livre = Livre("Titre", "Auteur", 2000)
        
        # Ajouter, réserver, annuler plusieurs fois
        bib.ajouter_livre(livre)
        livre.reserver()
        livre.annuler_reservation()
        livre.reserver()
        
        self.assertTrue(livre.reserve)
        self.assertEqual(bib.compter_livres_reserves(), 1)


if __name__ == '__main__':
    unittest.main()
