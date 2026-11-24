"""Ordonnancement des concerts sans chevauchement (1.5).

Algorithme de programmation dynamique (Weighted Interval Scheduling) :
- on trie les concerts par heure de fin
- pour chaque concert, on cherche le dernier concert compatible avant lui
- on remplit un tableau dp où chaque case donne le score maximal possible
- on remonte la solution pour retrouver les concerts choisis

Analyse de la complexité :
- Tri par heure de fin en O(n log n).
- Recherche du concert précédent compatible en O(n) par concert, donc O(n²) au total car on parcourt les concerts précédents à chaque étape.
- Programmation dynamique en O(n) car on remplit le tableau en une seule passe.
La complexité globale est donc en O(n²), dominée par la recherche des concerts précédents compatibles.
"""
from datetime import datetime


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


def chercher_precedent_compatible(concerts, i, trajet=0):
    """Cherche le dernier concert avant concerts[i] qui ne se chevauche pas."""
    debut_i = concerts[i].debut
    lieu_i = concerts[i].lieu

    for j in range(i - 1, -1, -1):
        fin_j = concerts[j].fin
        lieu_j = concerts[j].lieu
        delai = temps_trajet_entre(lieu_j, lieu_i, trajet)
        # on vérifie que le temps écoulé entre la fin de j et le début de i couvre le trajet
        if vers_minutes(debut_i, fin_j) >= delai:
            return j
    return -1


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

    # 2. pour chaque concert, indice du dernier concert compatible
    precedent = []
    for i in range(n):
        precedent.append(chercher_precedent_compatible(tries, i, trajets))

    # 3. programmation dynamique
    dp = [0.0] * (n + 1)
    for i in range(1, n + 1):
        c = tries[i - 1]
        p = precedent[i - 1]
        score_avec = c.score
        if p != -1:
            score_avec = score_avec + dp[p + 1]
        score_sans = dp[i - 1]
        if score_avec > score_sans:
            dp[i] = score_avec
        else:
            dp[i] = score_sans

    # 4. on remonte la solution pour retrouver les concerts choisis
    choisis = []
    curr = n
    while curr > 0:
        c = tries[curr - 1]
        p = precedent[curr - 1]
        score_avec = c.score
        if p != -1:
            score_avec = score_avec + dp[p + 1]
        score_sans = dp[curr - 1]
        if score_avec > score_sans:
            choisis.append(c)
            curr = p + 1
        else:
            curr = curr - 1

    choisis.reverse()
    return choisis, round(dp[n], 4)
