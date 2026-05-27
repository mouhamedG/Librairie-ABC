# Librairie ABC – Modernisation et Sécurisation d’une Application Web

## Objectif du projet

Ce projet consiste à reprendre une application web existante de gestion de bibliothèque ("Librairie ABC") afin d’améliorer :

- la sécurité ;
- la qualité du code ;
- la maintenabilité ;
- les performances ;
- la qualité des tests ;
- la préparation au déploiement sécurisé.

Le projet doit être mené selon une approche Agile et produire une version modernisée, sécurisée et documentée de l’application.

---

# Objectifs techniques

L’application existante doit être analysée, sécurisée, testée et améliorée.

Le travail doit inclure :

1. une revue complète du code existant ;
2. l’identification des vulnérabilités et mauvaises pratiques ;
3. la mise en place de correctifs de sécurité ;
4. l’amélioration de la structure du code ;
5. la mise en place de tests automatisés ;
6. l’analyse de sécurité via des outils automatiques ;
7. la réécriture des spécifications ;
8. la préparation d’un plan de déploiement sécurisé ;
9. une documentation claire du travail effectué.

---

# Structure attendue du repository

Le repository doit être organisé comme suit :

```txt
/
├── src/                    # Code source principal
├── tests/                  # Tests unitaires, fonctionnels et sécurité
├── docs/                   # Documentation technique et projet
├── reports/                # Rapports de sécurité et qualité
├── scripts/                # Scripts utilitaires
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Étape 1 — Analyse du code existant

Analyser complètement le code actuel afin d’identifier :

## Problèmes de sécurité
- routes non sécurisées ;
- accès non protégés ;
- mauvaise gestion des permissions ;
- absence de validation des entrées utilisateur ;
- vulnérabilités potentielles (injection SQL, XSS, accès non autorisés, exposition de données sensibles, etc.) ;
- gestion incorrecte des erreurs.

## Problèmes de qualité
- duplication du code ;
- fonctions trop longues ;
- mauvaise architecture ;
- faible lisibilité ;
- dette technique ;
- manque de modularité.

## Problèmes de performance
- traitements inutiles ;
- requêtes inefficaces ;
- logique peu optimisée.

Toutes les observations doivent être documentées.

---

# Étape 2 — Sécurisation de l’application

Implémenter des mesures de sécurité robustes.

## Gestion des routes et URLs
- sécuriser toutes les routes sensibles ;
- restreindre l’accès aux ressources critiques ;
- éviter l’exposition des chemins internes ;
- améliorer la gestion des URLs.

## Validation des données
Toutes les données utilisateur doivent être validées et nettoyées.

Prévoir :
- validation stricte des entrées ;
- gestion sécurisée des formulaires ;
- protection contre les injections ;
- prévention des comportements malveillants.

## Gestion des accès
Mettre en place :
- authentification sécurisée ;
- contrôle des permissions ;
- restriction d’accès selon les rôles.

---

# Étape 3 — Mise en place des tests

Créer une stratégie de tests automatisés.

Le projet doit inclure :

## Tests unitaires
Tester les fonctions critiques.

## Tests fonctionnels
Tester les comportements attendus de l’application.

## Tests de sécurité
Créer des scénarios de sécurité incluant :

- tests aux limites ;
- injections ;
- comportements inattendus ;
- simulations d’attaques ;
- tests de robustesse.

Tous les tests doivent être reproductibles.

---

# Étape 4 — Analyse automatisée du code

Configurer un outil d’analyse tel que SonarQube ou équivalent.

Objectifs :

- détecter les vulnérabilités ;
- mesurer la qualité du code ;
- détecter les mauvaises pratiques ;
- générer un rapport détaillé.

Chaque vulnérabilité doit être classée selon un niveau de risque :

- Critique
- Élevé
- Moyen
- Faible

Les résultats doivent être documentés dans `/reports`.

---

# Étape 5 — Refactoring du code

Améliorer la structure globale du projet.

Objectifs :

- améliorer la lisibilité ;
- réduire la complexité ;
- supprimer le code dupliqué ;
- séparer les responsabilités ;
- rendre le projet maintenable ;
- appliquer les bonnes pratiques de développement.

Le refactoring ne doit pas casser les fonctionnalités existantes.

---

# Étape 6 — Réécriture des spécifications

Réécrire les spécifications fonctionnelles et techniques après analyse du projet.

Inclure :

- comportements fonctionnels corrigés ;
- contraintes de sécurité ;
- nouvelles règles techniques ;
- architecture améliorée ;
- recommandations techniques.

---

# Étape 7 — Organisation Agile

Le projet doit suivre une méthode Agile.

Prévoir :

- répartition des rôles ;
- backlog des tâches ;
- sprint planning ;
- sprint review ;
- rétrospectives ;
- suivi des tâches.

Documenter le déroulement dans `/docs`.

---

# Étape 8 — Planification du déploiement sécurisé

Préparer le déploiement final.

Inclure :

## Environnement de test
Créer un environnement sécurisé de validation.

## Vérifications avant production
Valider :

- sécurité ;
- qualité du code ;
- stabilité ;
- réussite des tests.

## Déploiement
Prévoir :

- procédure de déploiement ;
- stratégie de rollback ;
- gestion des risques ;
- recommandations de mise en production.

---

# Livrables attendus

Le projet final doit contenir :

1. Une application sécurisée et améliorée.
2. Une revue documentée du code existant.
3. Des tests automatisés complets.
4. Un rapport d’analyse de sécurité.
5. Des propositions de refactoring.
6. Des spécifications réécrites.
7. Une documentation technique claire.
8. Un plan Agile documenté.
9. Une stratégie de déploiement sécurisé.
10. Une présentation finale (PDF ou PowerPoint).

---

# Instructions pour GitHub Copilot

Tu dois agir comme un ingénieur logiciel chargé de moderniser et sécuriser cette application.

Règles obligatoires :

- suivre les étapes du projet dans l’ordre ;
- documenter toutes les modifications ;
- ne jamais proposer une solution non sécurisée ;
- écrire du code maintenable ;
- proposer des améliorations progressives ;
- créer les tests associés à chaque modification ;
- produire des rapports exploitables ;
- respecter les exigences Agile ;
- prioriser la sécurité avant les nouvelles fonctionnalités.

Avant toute modification importante :

1. analyser ;
2. expliquer le problème ;
3. proposer une correction ;
4. implémenter ;
5. tester ;
6. documenter.