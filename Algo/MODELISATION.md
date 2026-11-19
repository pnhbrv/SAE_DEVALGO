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

## Tests

```
python -m pytest Algo -q
```
