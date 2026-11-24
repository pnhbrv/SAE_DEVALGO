# Analyse de la complexité (partie Planning, Cache et Recommandation)

Ce document détaille la complexité en temps et en espace des algorithmes écrits pour les parties **1.5** (`Algo/planning.py`), **1.6** (`Algo/cache.py`) et leur intégration dans `recommander(...)`.

Notations :
- $n$ : nombre de concerts dans la programmation (environ 80 concerts sur le festival).
- $k$ : nombre de concerts retenus dans le planning final ($k \le n$).
- $g$ : nombre maximal de genres associés à un concert (en pratique 1 à 3).
- $h$ : hauteur maximale de l'arbre des genres ($h = 3$ dans `STYLE_MUSICAL`).
- $s$ : nombre de spectateurs présents dans le cache en mémoire.

---

## 1. Scoring (`scoring.py` et `genres.py`)

Pour rappel, utilisé lors d'un défaut de cache :
- `ArbreGenres.remonter` / `preference_la_plus_proche` : remonte au plus $h$ parents via un dictionnaire Python (`O(1)` par saut), donc **$O(h) = O(1)$** puisque $h \le 3$.
- `score_concert` : évalue `score_genre` pour chacun des $g$ genres du concert, soit **$O(g \cdot h)$** (quasi constant en pratique).

---

## 2. Ordonnancement sans chevauchement (`planning.py`)

### Fonctions élémentaires
- `vers_minutes`, `heure_fin`, `temps_trajet_entre`, `sont_compatibles` : toutes en **$O(1)$** en temps et en espace.

### `planifier_concerts(concerts, trajets=0)`
1. **Filtrage des concerts à score positif** : parcours linéaire des $n$ concerts en **$O(n)$**. Soit $m \le n$ le nombre de candidats retenus.
2. **Tri par heure de fin** (`sorted(candidats, key=heure_fin)`) : **$O(m \log m)$** en temps (Timsort), $O(m)$ en espace.
3. **Programmation dynamique** :
   - Pour chaque concert $i \in \{0, \dots, m-1\}$, on parcourt tous les concerts précédents $j \in \{0, \dots, i-1\}$ et on teste `sont_compatibles(tries[j], tries[i], trajets)` en $O(1)$.
   - Nombre d'itérations : $\sum_{i=0}^{m-1} i = \frac{m(m-1)}{2}$, soit **$O(m^2)$** en temps.
   - *Pourquoi ne pas descendre à $O(m \log m)$ avec une recherche dichotomique ?* Sans temps de trajet, la compatibilité ne dépend que de `fin[j] <= debut[i]`, donc le dernier concert compatible forme un préfixe monotone qu'on peut trouver par dichotomie. En présence d'un `trajets > 0` entre lieux différents, deux concerts $j_1 < j_2$ peuvent avoir le même horaire de fin ou presque, mais $j_1$ peut être dans le même lieu que $i$ (trajet nul, donc compatible) alors que $j_2$ est dans un autre lieu (trajet requis, donc incompatible). Vérifier tous les $j < i$ garantit l'optimalité quel que soit le lieu.
4. **Recherche du maximum et reconstruction du planning** :
   - Parcours de `meilleur` : $O(m)$.
   - Remontée de `avant` puis `choisis.reverse()` : $O(k) \le O(m)$.

**Bilan pour `planifier_concerts` :**
- **Temps :** $O(n + m \log m + m^2) = \mathbf{O(n^2)}$ dans le pire cas (et $O(1)$ si aucun concert n'a de score positif).
- **Espace :** $\mathbf{O(n)}$ (tableaux `candidats`, `tries`, `meilleur`, `avant`, `choisis`).

---

## 3. Cache et recommandation complète (`cache.py`)

### `CacheRecommandations`
Le cache repose sur une table de hachage Python (`self.entrees` : dictionnaire `id_spectateur -> dict`) :
- `est_valide` : accès au dictionnaire et comparaisons simples → **$O(1)$** en temps.
- `obtenir` : accès direct par clé → **$O(1)$** en temps.
- `enregistrer` : insertion/mise à jour par clé → **$O(1)$** amorti en temps.
- `invalider(id_spectateur)` : suppression par clé → **$O(1)$** amorti en temps (`invalider(None)` vide tout le dictionnaire en $O(s)$).
- **Mémoire du cache :** $O(s \cdot k)$ où $k$ est le nombre moyen de concerts recommandés par spectateur.

### `recommander(...)`
- **Meilleur cas (cache valide / *cache hit*) :**
  `est_valide` + `obtenir` → **$\mathbf{O(1)}$** en temps (aucun score recalculé, aucune programmation dynamique exécutée).
- **Pire cas (cache absent ou périmé / *cache miss*) :**
  1. Vérification du cache : $O(1)$.
  2. Calcul du score des $n$ concerts : $O(n \cdot g \cdot h)$.
  3. Appel à `planifier_concerts` : $O(n^2)$.
  4. Mise en cache : $O(1)$.
  - **Complexité globale lors d'un recalcul :** $\mathbf{O(n \cdot g \cdot h + n^2)}$. Comme $g$ et $h$ sont très petits et bornés ($h \le 3$), le terme quadratique $O(n^2)$ domine dès que $n$ grandit.

---

## 4. Ordre de grandeur sur Festiut'O

Avec environ $n = 80$ concerts :
- $n^2 / 2 \approx 3\,200$ comparaisons dans la programmation dynamique, soit moins d'une milliseconde en Python.
- Une fois calculée, chaque consultation suivante par le même spectateur (tant que la programmation et ses préférences ne changent pas) s'exécute en temps constant $O(1)$.
