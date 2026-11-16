# SAE 3.01 Festiut'O — À faire (Algo + Dev Web)

> Période : 14/09/26 → 05/12/26 (échéance à confirmer pour l'Algo)
> Équipe : 4 personnes (2 Algo, 2 Web)
> Le planning prévisionnel ne se modifie jamais : on ajoute un planning effectif à côté, avec l'explication des écarts.

---

## 1. Partie Algo (2 personnes)

### 1.1 Schéma BDD (à modifier, exigé par le sujet)
-  Table `Genre` avec hiérarchie (`id_genre_parent` → `Genre`)
-  Table des préférences festivalier ↔ genre (signe positif/négatif, note éventuelle, ex. -5 à +5)
-  Association concert ↔ genres (N-N) pour le cas multi-genres
-   Table de cache des recommandations (festivalier, concert, score, version/horodatage)
-   Mettre à jour le MCD / MLD / scripts SQL

### 1.2 Modélisation
-   Choisir et justifier la structure de données de l'arbre des genres (parent, enfants, profondeur)
-   Définir la distance entre un genre et une préférence (ex. nombre d'arêtes en remontant)
-   Choisir la structure des préférences (ex. dictionnaire `genre → note`)

### 1.3 Algorithme mono-genre (priorité)
-   Remonter la hiérarchie depuis le genre du concert
-   Garder la préférence la plus proche (gère « le rock sauf le garage rock »)
-   Préférence négative → concert écarté
-   Préférence positive → bon candidat avec un score
-   Aucune préférence → proposable mais non prioritaire
-   Départage entre concerts (note + distance, ex. `score = note / (1 + distance)`)

### 1.4 Généralisation multi-genres
-   Noter un concert à partir de tous ses genres (meilleur sous-genre ou moyenne pondérée)
-   Décider et documenter le cas d'un seul genre négatif parmi plusieurs

### 1.5 Compatibilité avec le planning
-   Ne jamais proposer deux concerts en parallèle
-   Sélectionner l'ensemble de concerts sans chevauchement qui maximise le score (programmation dynamique, *weighted interval scheduling*)
-   Gérer les journées 14h → 4h (passage de minuit)
-   Décider si on tient compte du temps de trajet entre lieux

### 1.6 Cache des recommandations
-   Interroger le cache en priorité avant tout calcul
-   Recalculer uniquement si la programmation change ou si les préférences changent
-   Mécanisme d'invalidation (numéro de version de la programmation ou horodatage)

### 1.7 Implémentation et tests
-   Implémentation Python des algorithmes
-   Jeux d'essai : arbre de genres réaliste, plusieurs profils, cas limites
-   Tests unitaires + analyse de complexité

### 1.8 Bonus (si le temps le permet) : « Vous aimerez peut-être »
-   Exploiter les données de l'enquête de satisfaction (historique)
-   Générer une nouvelle hiérarchie de genres (co-appréciation + clustering hiérarchique)
-   Proposer des recommandations hors préférences déclarées

---

## 2. Partie Dev Web (2 personnes)

Stack imposée par les ressources : Flask (R3.01), développement efficace (R3.02), qualité (R3.04), SQL dans un langage de programmation (R3.07).

### 2.1 Côté spectateur
-   Programmation par journée (14h → 4h), par lieu, par artiste
-   Fiche groupe : description, photos, réseaux sociaux, vidéos, membres et instruments, style
-   Recherche par style, sous-genres inclus (dépend de la hiérarchie de l'Algo)
-   Groupes favoris et organisation de sa journée
-   Groupes similaires sur la fiche d'un groupe
-   Achat de billets (jour, 2 jours, festival entier)
-   Concerts gratuits (accès libre)
-   Pré-inscription pour les lieux à jauge limitée
-   Affichage des recommandations (module Algo + cache)

### 2.2 Côté organisateur (back-office)
-   CRUD de la programmation (concerts, lieux, groupes)
-   Par groupe : jour/heure d'arrivée et de départ, durée du concert, temps de montage et de démontage
-   Affectation d'un hébergement avec nombre de places (capacité limitée par jour)
-   Vérification de cohérence de la programmation (temps entre concerts d'un même groupe, arrivée assez tôt, fin pas trop tard)
-   Activités annexes (interviews, showcases…) : lieu, heure, visible ou non dans la programmation

### 2.3 Transversal
-   Authentification et rôles (visiteur, spectateur, organisateur)
-   Sécurité : hash des mots de passe, CSRF, requêtes SQL paramétrées
-   Accessibilité et ergonomie (AC21.02)
-   Tests unitaires : modèle, URLs, formulaires, vues
-   Tests d'intégration selon les scénarios métiers
-   Coverage et critères d'acceptation (% asserts, % couverture)
-   Tests de performances et de sécurité

---

## 3. Interface Algo ↔ Web
-   Définir tôt le contrat, ex. `recommander(id_festivalier) -> liste de concerts`
-   Brancher le cache sur la BDD de l'application

---

## 4. Livrables communs

### 4.1 Suivi de projet
-   Liste des tâches chiffrées et attribuées
-   Planning prévisionnel (jamais modifié)
-   Planning effectif + explication des écarts
-   Backlog à jour
-   Présentation de l'outil de suivi

### 4.2 Dossier de spécifications fonctionnelles et techniques (SFD/STD)
-   Page de garde, sommaire, introduction (contexte, périmètre inclus/exclu)
-   **Fonctionnel** : acteurs et rôles, cas d'utilisation, diagrammes UML (séquence, activité), règles de gestion, maquettes/wireframes, MCD, dictionnaire de données, contraintes non fonctionnelles
-   **Technique** : architecture, technologies, MLD/MPD, index/triggers/procédures, protocoles et formats d'échange, normes de développement, environnements, versionning
-   **Tests** : jeux de données, critères d'acceptation, plan de tests (unitaire, intégration, performances, sécurité)
-   Annexes éventuelles (glossaire, références)

### 4.3 Autres livrables
-   Code documenté selon les règles de l'art
-   Jeux d'essais et résultats des tests avec coverage
-   Guide d'utilisation (rédigé pour l'utilisateur final)
-   Vidéo de présentation ou soutenance (à définir avec l'enseignant référent)
-   Rapport individuel (AC26.04) : compétences mises en œuvre, avec exemples concrets

### 4.4 Dépôt GitHub
-   Commits clairs, issues, backlog, PR, reviews, branches visibles dans le dépôt
-   Code final et progression de la SAE présentés dans le dépôt

---

## 5. À clarifier
-   Même date de rendu pour l'Algo et le Web (5/12) ou échéance séparée ?
-   Algo intégré à l'application Flask ou module Python séparé ?
-   SGBD utilisé (SQLite, MySQL, PostgreSQL) ?
-   Squelette Flask existant ou à créer ?
-   Données de l'enquête de satisfaction et jeu de genres disponibles ?
-   Répartition nominative des 4 personnes