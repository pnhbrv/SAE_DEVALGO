"""Score d'un concert pour un cleint, à partir de ses préférences de genres

Les préférences sont un dictionnaire {id_genre: note}, avec une note de -5 à +5
Un genre absent du dictionnaire = pas de préférence.
"""

SCORE_NEUTRE = 0.05   # aucune préférence : le concert reste proposable, mais jamais en premier


def preference_la_plus_proche(arbre, prefs, id_genre):
    """Remonte l'arbre depuis le genre et renvoie (note, distance) de la première
    préférence. Renvoie None s'il n'y en a aucune."""
    for genre, distance in arbre.remonter(id_genre):
        if genre in prefs:
            return prefs[genre], distance
    return None


def score_genre(arbre, prefs, id_genre):
    """Score d'un concert qui a un seul genre.

    - préférence négative : on renvoie None
    - préférence positive : note / (1 + distance)
    - aucune préférence : SCORE_NEUTRE
    """
    trouve = preference_la_plus_proche(arbre, prefs, id_genre)
    if trouve is None:
        return SCORE_NEUTRE
    note, distance = trouve
    if note < 0:
        return None
    return note / (1 + distance)


def score_concert(arbre, prefs, genres, strategie="max", ecarter_si_negatif=True):
    """Score d'un concert qui peut avoir plusieurs genres. None = concert écarté.

    ecarter_si_negatif=True  : un seul genre négatif suffit à écarter le concert.
    ecarter_si_negatif=False : on ignore les genres négatifs et on garde les autres.
    strategie : "max" (on garde le meilleur score) ou "moyenne".
    """
    scores = []
    for genre in genres:
        scores.append(score_genre(arbre, prefs, genre))

    if len(scores) == 0:
        return SCORE_NEUTRE

    if ecarter_si_negatif and None in scores:
        return None

    # on enlève les genres écartés (None)
    valides = []
    for s in scores:
        if s is not None:
            valides.append(s)
    if len(valides) == 0:
        return None

    if strategie == "max":
        return max(valides)
    return sum(valides) / len(valides)
