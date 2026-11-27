# Modélisation de la partie Algo

Les choix qu'on a faits pour la recommandation de concerts.

## L'arbre des genres

Les genres viennent de la table `STYLE_MUSICAL`. Chaque style a un parent (`id_style_parent`), sauf les 13 genres du haut (Rock, Pop, Hip-hop...) qui n'en ont pas. Il y a 3 niveaux au maximum : genre, sous-genre, sous-sous-genre.

Dans le code, on stocke ça dans un dictionnaire `{id_genre: id_parent}`. On n'a pas besoin de plus : tout ce qu'on fait, c'est partir d'un genre et remonter vers son parent, donc le dictionnaire suffit.

## La distance

La distance entre un genre et une préférence, c'est le nombre de fois qu'on remonte dans l'arbre.

Exemple : Garage punk est dans Garage rock, qui est dans Rock.

- Garage punk : distance 0
- Garage rock : distance 1
- Rock : distance 2

## Les préférences

Un festivalier note des genres de -5 à +5 (jamais 0). Si un genre n'a pas de note, il n'a pas de préférence. On les met dans un dictionnaire `{id_genre: note}`.

Pour un concert, on remonte l'arbre depuis son genre et on garde la première note qu'on trouve, donc la plus proche. C'est ce qui permet de dire "j'aime le rock sauf le garage rock".

## Le score d'un concert (un seul genre)

- Note négative : le concert est écarté.
- Note positive : `score = note / (1 + distance)`. Plus la note est loin dans l'arbre, moins elle compte.
- Pas de note : score de 0,05. Le concert peut être proposé mais jamais en premier.

Exemple avec Rock à +5 et Garage rock à -3 :

| Concert | Résultat |
|---|---|
| Rock | 5 |
| Folk rock | 5 / 2 = 2,5 |
| Garage rock | écarté |
| Garage punk | écarté (il prend la note du Garage rock) |
| Pop | 0,05 |

## Plusieurs genres

Un concert peut avoir plusieurs genres. On calcule le score de chaque genre, puis on les rassemble :

- si un des genres est négatif, on écarte le concert (on peut changer ça avec `ecarter_si_negatif=False`) ;
- sinon on prend le meilleur score (ou la moyenne avec `strategie="moyenne"`).

## Choisir les concerts sans chevauchement (1.5)

Même avec de bons scores, on ne peut pas aller à deux concerts en même temps. Il faut donc choisir, parmi les concerts conseillés, ceux qui ne se chevauchent pas et dont la somme des scores est la plus grande. On ne garde que les concerts qui ont un score positif.

Prendre le concert au meilleur score ne suffit pas. Exemple : un concert de 14h à 17h (score 10), un de 16h à 19h (score 15) et un de 18h à 21h (score 10). Si on prend le meilleur score (15), on ne peut plus voir les deux autres. Mais le premier et le troisième ne se chevauchent pas et font 20 à eux deux.

On utilise donc la programmation dynamique :

1. On trie les concerts par heure de fin.
2. Pour chaque concert, on calcule le meilleur total d'un planning qui finit par lui : son score, plus le meilleur total parmi les concerts d'avant qui sont déjà finis quand il commence.
3. On prend le meilleur total, puis on remonte concert par concert pour retrouver le planning.

Les concerts ont une date et une heure complètes, donc une journée qui passe minuit (un concert de 23h à 0h30, puis un autre à 1h) ne pose pas de problème.

**Temps de trajet :** il y a une option `trajets` (en minutes). Si deux concerts sont dans des lieux différents, il faut que le trajet tienne entre la fin du premier et le début du second. Par défaut c'est 0 : on ne compte pas le trajet.

## Le cache (1.6)

Calculer les scores et le planning à chaque visite est inutile si rien n'a changé. Le cache garde le résultat de chaque festivalier. Il est encore valable si :

- le numéro de version de la programmation est le même (il augmente quand un concert est ajouté, modifié ou supprimé) ;
- le festivalier n'a pas modifié ses préférences depuis le calcul.

La fonction `recommander` regarde d'abord le cache. S'il est valable, elle renvoie le résultat tout de suite. Sinon, elle note chaque concert, choisit le planning, enregistre le résultat dans le cache, puis le renvoie.

**Limite :** pour l'instant le cache est un simple dictionnaire Python. Il est perdu quand le site redémarre. Les tables `CALCUL_RECOMMANDATION`, `CACHE_RECOMMANDATION` et `VERSION_PROGRAMMATION` existent dans la base, avec leurs triggers, mais le code Python ne les utilise pas encore.

## Complexité

On note `n` le nombre de concerts (environ 80 au festival), `g` le nombre de genres d'un concert et `h` la hauteur de l'arbre (3 au maximum).

**Score**
- Score d'un genre : on remonte au plus `h` niveaux, chaque saut est une lecture de dictionnaire. C'est donc en O(h), soit O(1) puisque `h` ≤ 3.
- Score d'un concert : au plus `g` remontées, donc O(g × h).

**Planning (`planifier_concerts`)**
- On garde les concerts de score positif : O(n).
- On les trie par heure de fin : O(n log n).
- Programmation dynamique : pour chaque concert, on regarde tous les précédents. Cela fait 1 + 2 + … + (n−1) = n(n−1)/2 comparaisons, donc O(n²). C'est cette étape qui domine.
- On ne peut pas descendre à O(n log n) avec une recherche dichotomique à cause des trajets : deux concerts qui finissent presque en même temps peuvent être l'un dans le même lieu (compatible), l'autre dans un autre lieu (trajet trop long). Il faut donc tester tous les précédents.
- Reconstruction du planning : O(n).
- Mémoire : O(n) (les listes `meilleur` et `avant`).

**Cache**
- Valable, obtenir, enregistrer, invalider : une lecture ou écriture dans un dictionnaire, donc O(1). Vider tout le cache coûte O(s), avec `s` le nombre de spectateurs.
- Mémoire : O(s × k), avec `k` le nombre de concerts recommandés par spectateur.

**Une recommandation complète (`recommander`)**
- Cache valable : O(1), rien n'est recalculé.
- Cache absent ou périmé : `n` scores en O(n × g × h), puis le planning en O(n²). Au total O(n²).

Avec `n` = 80, le planning fait environ 3 200 comparaisons, ce qui prend moins d'une milliseconde en Python. Ensuite, tant que la programmation et les préférences ne changent pas, le même spectateur obtient sa liste en temps constant.

## Tests

Les tests sont dans `Algo/`, un fichier par sujet :

- `test_genres.py` et `test_scoring.py` : l'arbre et le score, sur un petit arbre (`jeu_essai.py`).
- `test_arbre_reel.py` et `test_profils.py` : l'arbre de 273 styles et les profils d'Emma, Louis, Chloé et Thomas (`profils.py`).
- `test_planning.py` : le choix des concerts sans chevauchement, la programmation dynamique contre le choix glouton, le passage de minuit et le trajet.
- `test_cache.py` : le cache valable, périmé, invalidé.

```
python -m pytest Algo -q
```
