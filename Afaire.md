# SAE 3.01 Festiut'O : ce qu'il nous reste à faire (Algo + Dev Web)

> Période : du 14/09/26 au 05/12/26 (la date de rendu de l'Algo reste à confirmer)
> Équipe : 4 personnes (2 sur l'Algo, 2 sur le Web)
> Le planning prévisionnel ne change jamais. À côté, on tient un planning effectif et on explique les écarts.

---

## 1. Partie Algo (2 personnes)

### 1.1 Schéma de la base de données (à modifier, le sujet l'exige)
- Une hiérarchie de genres : une table `Genre` où chaque genre pointe vers son parent (`id_genre_parent`)
- Les préférences de chaque festivalier pour un genre : positive ou négative, avec une note (par exemple de -5 à +5)
- Le lien entre un concert et ses genres (plusieurs genres possibles pour un même concert)
- Un cache des recommandations : pour chaque festivalier et chaque concert, le score et la version ou la date du calcul
- Mettre à jour le MCD, le MLD et les scripts SQL

### 1.2 Modélisation
- Choisir comment représenter l'arbre des genres (parent, enfants, profondeur) et expliquer pourquoi
- Définir la distance entre un genre et une préférence (par exemple le nombre d'étapes en remontant dans l'arbre)
- Choisir comment stocker les préférences (par exemple un dictionnaire `genre → note`)

### 1.3 Algorithme pour un concert à un seul genre (la priorité)
- Partir du genre du concert et remonter dans la hiérarchie
- Préférence négative : on écarte le concert
- Préférence positive : le concert est un bon candidat, avec un score
- Aucune préférence : on peut le proposer, mais sans le mettre en avant
- Départager les concerts avec la note et la distance (par exemple `score = note / (1 + distance)`)

### 1.4 Concerts avec plusieurs genres
- Noter le concert à partir de tous ses genres (le meilleur sous-genre, ou une moyenne pondérée)
- Décider ce qu'on fait quand un seul genre est négatif parmi plusieurs, et l'écrire

### 1.5 Respecter le planning
- Ne jamais proposer deux concerts qui se jouent en même temps
- Choisir l'ensemble de concerts qui ne se chevauchent pas et qui donne le meilleur score total (programmation dynamique, *weighted interval scheduling*)
- Gérer les journées qui vont de 14h à 4h du matin (le passage de minuit)
- Décider si on tient compte du temps de trajet entre deux lieux

### 1.6 Cache des recommandations
- Regarder dans le cache avant de calculer quoi que ce soit
- Ne recalculer que si la programmation ou les préférences ont changé
- Prévoir comment on sait que le cache est périmé (un numéro de version de la programmation ou une date)

### 1.7 Code et tests
- Écrire les algorithmes en Python
- Préparer des jeux d'essai : un arbre de genres réaliste, plusieurs profils de festivaliers et des cas limites
- Écrire les tests unitaires et analyser la complexité

### 1.8 Bonus, si on a le temps : « Vous aimerez peut-être »
- Utiliser les données de l'enquête de satisfaction (l'historique)
- Construire une nouvelle hiérarchie de genres (genres souvent appréciés ensemble, puis regroupement hiérarchique)
- Proposer des recommandations en dehors des préférences déclarées

---

## 2. Partie Dev Web (2 personnes)

Les technologies viennent des ressources du cours : Flask (R3.01), développement efficace (R3.02), qualité (R3.04) et SQL dans un langage de programmation (R3.07).

### 2.1 Côté spectateur
- Voir la programmation par journée (de 14h à 4h), par lieu et par artiste
- Fiche d'un groupe : description, photos, réseaux sociaux, vidéos, membres avec leurs instruments, style
- Chercher par style, sous-genres compris (ça dépend de la hiérarchie faite par l'Algo)
- Gérer ses groupes favoris et organiser sa journée
- Voir des groupes similaires sur la fiche d'un groupe
- Acheter des billets (une journée, deux jours ou tout le festival)
- Concerts gratuits (accès libre)
- Se pré-inscrire pour les lieux qui ont une jauge limitée
- Voir ses recommandations (module Algo + cache)

### 2.2 Côté organisateur (back-office)
- Créer, modifier et supprimer la programmation (concerts, lieux, groupes)
- Pour chaque groupe : jour et heure d'arrivée et de départ, durée du concert, temps de montage et de démontage
- Attribuer un hébergement avec un nombre de places (la capacité est limitée par jour)
- Vérifier que la programmation tient la route (assez de temps entre deux concerts d'un même groupe, arrivée assez tôt, fin pas trop tard)
- Activités annexes (interviews, showcases…) : lieu, heure, et visible ou non dans la programmation

### 2.3 Pour tout le site
- Connexion et rôles (visiteur, spectateur, organisateur)
- Sécurité : mots de passe hachés, protection CSRF, requêtes SQL paramétrées
- Accessibilité et confort d'utilisation (AC21.02)
- Tests unitaires : modèle, URLs, formulaires, vues
- Tests d'intégration à partir des scénarios métier
- Couverture de tests et critères d'acceptation (% d'assertions, % de couverture)
- Tests de performances et de sécurité

---

## 3. Lien entre l'Algo et le Web
- Se mettre d'accord tôt sur ce que l'Algo fournit, par exemple `recommander(id_festivalier) -> liste de concerts`
- Brancher le cache sur la base de données de l'application

---

## 4. Livrables communs

### 4.1 Suivi du projet
- La liste des tâches, chiffrées et attribuées
- Le planning prévisionnel (on n'y touche jamais)
- Le planning effectif, avec l'explication des écarts
- Un backlog à jour
- La présentation de l'outil de suivi

### 4.2 Dossier de spécifications fonctionnelles et techniques (SFD/STD)
- Page de garde, sommaire, introduction (contexte, ce qui est inclus et ce qui ne l'est pas)
- **Fonctionnel** : acteurs et rôles, cas d'utilisation, diagrammes UML (séquence, activité), règles de gestion, maquettes, MCD, dictionnaire de données, contraintes non fonctionnelles
- **Technique** : architecture, technologies, MLD et MPD, index, triggers et procédures, formats d'échange, normes de développement, environnements, gestion des versions
- **Tests** : jeux de données, critères d'acceptation, plan de tests (unitaires, intégration, performances, sécurité)
- Annexes si besoin (glossaire, références)

### 4.3 Autres livrables
- Un code bien documenté, dans les règles de l'art
- Les jeux d'essai et les résultats des tests, avec la couverture
- Un guide d'utilisation, écrit pour l'utilisateur final
- Une vidéo de présentation ou une soutenance (à voir avec l'enseignant référent)
- Le rapport individuel (AC26.04) : les compétences mobilisées, avec des exemples concrets

### 4.4 Dépôt GitHub
- Des commits clairs, des issues, un backlog, des PR, des relectures et des branches visibles
- Le code final et l'avancement de la SAE visibles dans le dépôt

---

## 5. Ce qu'il faut encore éclaircir
- Est-ce que l'Algo et le Web rendent le même jour (le 5/12), ou chacun a sa date ?
- L'algo est-il intégré à l'application Flask, ou c'est un module Python à part ?
- Quel SGBD utilise-t-on (SQLite, MySQL, PostgreSQL) ?
- Y a-t-il déjà un squelette Flask, ou faut-il le créer ?
- A-t-on les données de l'enquête de satisfaction et une liste de genres ?
- Qui fait quoi : voir la proposition en section 6, à valider ensemble

---

## 6. Qui fait quoi (proposition à valider ensemble)

- **Algo** : Gihed et Adam
- **Dev Web** : Yael et Rayan

### 6.1 Algo

| Section | Tâche | Qui |
|---|---|---|
| 1.2 | Modélisation : l'arbre, la distance, les préférences (`Algo/MODELISATION.md`) | Gihed |
| 1.3 | Algorithme pour un seul genre | Gihed |
| 1.4 | Concerts à plusieurs genres, et décision sur le genre négatif | Gihed |
| 1.1 | Schéma de la base : `PREFERENCE_STYLE`, `VERSION_PROGRAMMATION`, `CACHE_RECOMMANDATION`, MCD, MLD et SQL | Adam |
| 1.5 | Planning sans chevauchement (programmation dynamique, minuit, trajet) | Adam |
| 1.6 | Cache des recommandations et mise à jour quand il est périmé | Adam |
| 1.7 | Tests, jeux d'essai et complexité (chacun pour sa partie) | Gihed et Adam |
| 1.8 | Bonus « Vous aimerez peut-être » (si on a le temps) | Gihed et Adam |

Adam prévient Rayan et Yael avant de toucher à `Creation.sql`, puisque la partie BDD est la leur.

### 6.2 Dev Web

| Section | Tâche | Qui |
|---|---|---|
| 2.1 | Programmation par journée, lieu et artiste | Yael |
| 2.1 | Fiche d'un groupe | Yael |
| 2.1 | Recherche par style (sous-genres compris) | Yael |
| 2.1 | Favoris, organisation de la journée, groupes similaires | Yael |
| 2.1 | Affichage des recommandations (appel au module Algo) | Yael |
| 2.1 | Achat de billets, concerts gratuits, pré-inscription | Rayan |
| 2.2 | Back-office : programmation, hébergements, vérification de cohérence, activités annexes | Rayan |
| 2.3 | Connexion, rôles et sécurité (hachage, CSRF, SQL paramétré) | Rayan |
| 2.3 | Accessibilité, ergonomie et tests unitaires (modèle, URLs, formulaires, vues) | Yael |
| 2.3 | Tests d'intégration, de performances et de sécurité, couverture | Rayan |

### 6.3 Lien entre l'Algo et le Web (section 3)
- Gihed et Adam définissent ce que renvoie `recommander(...)`, et Yael l'intègre dans Flask.
- Adam et Rayan branchent le cache sur la base de l'application.

### 6.4 Livrables communs (section 4)
- Suivi du projet (4.1) : Yael, comme cheffe de projet. Chacun met à jour ses propres tâches.
- SFD/STD (4.2) : chaque binôme écrit sa partie, et Yael assemble le tout.
- Rapport individuel et dépôt GitHub (4.3 et 4.4) : chacun fait le sien, avec des commits, issues et PR propres.
- Guide d'utilisation : l'équipe Web. Vidéo ou soutenance : tous les quatre.
