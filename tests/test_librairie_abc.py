"""
Tests unitaires pour la bibliothèque ABC
"""

import unittest
import sys
from pathlib import Path

# Ajouter le répertoire src au chemin Python pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from librairie_abc import Livre, Bibliotheque
from exceptions import LivreAlreadyReservedError, LivreNotReservedError


class TestBibliotheque(unittest.TestCase):
    """Tests pour la classe Bibliotheque."""
    
    def setUp(self):
        self.bibliotheque = Bibliotheque()
        self.livre1 = Livre("Le Petit Prince", "Antoine de Saint-Exupéry", 1943)
        self.bibliotheque.ajouter_livre(self.livre1)

    def test_ajout_et_liste_de_livres(self):
        """Ajouter un livre et le lister doit fonctionner."""
        self.assertIn("Le Petit Prince", self.bibliotheque.lister_livres())

    def test_reservation_livre(self):
        """Réserver un livre doit retourner un message et changer l'état."""
        message = self.livre1.reserver()
        self.assertIn("réservé", message)
        self.assertTrue(self.livre1.reserve)
        
        # Réserver deux fois doit lever une exception
        with self.assertRaises(LivreAlreadyReservedError):
            self.livre1.reserver()

    def test_annulation_reservation(self):
        """Annuler la réservation doit fonctionner."""
        self.livre1.reserver()
        message = self.livre1.annuler_reservation()
        self.assertIn("annulée", message)
        self.assertFalse(self.livre1.reserve)
        
        # Annuler deux fois doit lever une exception
        with self.assertRaises(LivreNotReservedError):
            self.livre1.annuler_reservation()


if __name__ == '__main__':
    unittest.main()
