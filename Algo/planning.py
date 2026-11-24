"""Ordonnancement des concerts sans chevauchement (1.5).

Programmation dynamique :
- on trie les concerts par heure de fin
- pour chaque concert i, on regarde tous les concerts j d'avant et on garde celui
  qui donne le meilleur total une fois compatible avec i
- meilleur[i] = score de i + meilleur total d'un planning qui finit par un concert compatible
- on remonte la chaîne pour retrouver les concerts choisis

Complexité : le tri est en O(n log n), puis deux boucles imbriquées en O(n²).
La complexité globale est en O(n²).
"""

def vers_minutes(a, b):
    """Calcule la différence en minutes entre deux datetime (a - b)."""
    return (a - b).total_seconds() / 60


def heure_fin(concert):
    """Renvoie l'heure de fin d'un concert (utilisé pour le tri sans lambda)."""
    return concert.fin


def temps_trajet_entre(lieu_a, lieu_b, trajet=0):
    """Temps de déplacement en minutes entre deux lieux.

    Si les deux concerts sont dans le même lieu, ou si un lieu est None,
    le trajet est nul (0 minute).
    """
    if trajet is None or lieu_a is None or lieu_b is None or lieu_a == lieu_b:
        return 0
    return trajet


def sont_compatibles(concert_avant, concert_apres, trajet=0):
    """Vrai si on peut voir concert_apres après concert_avant : il faut que le premier
    soit fini, et qu'il reste le temps du trajet si les deux lieux sont différents."""
    delai = temps_trajet_entre(concert_avant.lieu, concert_apres.lieu, trajet)
    return vers_minutes(concert_apres.debut, concert_avant.fin) >= delai


def planifier_concerts(concerts, trajets=0):
    """Choisit les concerts qui ne se chevauchent pas avec le meilleur score total.

    Renvoie (liste_concerts, score_total).
    """
    # on ne garde que les concerts qui ont un score positif
    candidats = []
    for c in concerts:
        if c.score is not None and c.score > 0:
            candidats.append(c)

    if len(candidats) == 0:
        return [], 0.0

    # 1. tri par heure de fin
    tries = sorted(candidats, key=heure_fin)
    n = len(tries)

    # 2. meilleur[i] = meilleur score total d'un planning qui finit par le concert i
    #    avant[i] = le concert qui précède i dans ce planning (-1 s'il n'y en a pas)
    meilleur = []
    avant = []
    for i in range(n):
        meilleur.append(tries[i].score)
        avant.append(-1)
        for j in range(i):
            if sont_compatibles(tries[j], tries[i], trajets):
                if meilleur[j] + tries[i].score > meilleur[i]:
                    meilleur[i] = meilleur[j] + tries[i].score
                    avant[i] = j

    # 3. le meilleur planning finit par le concert qui a le meilleur total
    dernier = 0
    for i in range(n):
        if meilleur[i] > meilleur[dernier]:
            dernier = i

    # 4. on remonte la chaîne pour retrouver les concerts choisis
    choisis = []
    i = dernier
    while i != -1:
        choisis.append(tries[i])
        i = avant[i]
    choisis.reverse()
    return choisis, round(meilleur[dernier], 4)
