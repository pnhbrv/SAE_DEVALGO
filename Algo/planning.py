"""Ordonnancement des concerts sans chevauchement (1.5).

Algorithme de programmation dynamique (Weighted Interval Scheduling) :
- on trie les concerts par heure de fin
- pour chaque concert, on cherche le dernier concert compatible avant lui
- on choisit d'ajouter le concert ou non selon ce qui rapporte le meilleur score total
- gestion de la journée de 14h à 4h du matin (passage de minuit)
- prise en compte facultative du temps de trajet entre deux lieux
"""
from datetime import datetime, time


def vers_minutes(horaire):
    """Convertit un horaire en minutes depuis le début de journée.

    Gère le passage de minuit : le festival va de 14h à 4h du matin.
    Une heure entre 00h et 05h appartient au créneau nocturne (on ajoute 24h).
    Fonctionne avec des chaînes 'HH:MM', des datetime, time ou des nombres.
    """
    if isinstance(horaire, (int, float)):
        return float(horaire)

    if isinstance(horaire, datetime):
        return horaire.timestamp() / 60.0

    if isinstance(horaire, time):
        heures = horaire.hour
        if heures < 12:
            heures = heures + 24
        return heures * 60 + horaire.minute + horaire.second / 60.0

    if isinstance(horaire, str):
        if " " in horaire or "T" in horaire:
            dt = datetime.fromisoformat(horaire)
            return dt.timestamp() / 60.0

        parties = horaire.split(":")
        heures = int(parties[0])
        minutes = int(parties[1])
        if heures < 12:
            heures = heures + 24
        return heures * 60 + minutes

    return 0.0


def temps_trajet_entre(lieu_a, lieu_b, trajets=None):
    """Temps de déplacement en minutes entre deux lieux."""
    if trajets is None or lieu_a is None or lieu_b is None or lieu_a == lieu_b:
        return 0.0
    if isinstance(trajets, (int, float)):
        return float(trajets)
    if isinstance(trajets, dict):
        return float(trajets.get((lieu_a, lieu_b), trajets.get((lieu_b, lieu_a), 0.0)))
    if callable(trajets):
        return float(trajets(lieu_a, lieu_b))
    return 0.0


def chercher_precedent_compatible(concerts, i, trajets=None):
    """Cherche le dernier concert avant concerts[i] qui ne se chevauche pas."""
    debut_i = vers_minutes(concerts[i].debut)
    lieu_i = concerts[i].lieu

    for j in range(i - 1, -1, -1):
        fin_j = vers_minutes(concerts[j].fin)
        lieu_j = concerts[j].lieu
        delai = temps_trajet_entre(lieu_j, lieu_i, trajets)
        if fin_j + delai <= debut_i:
            return j
    return -1


def planifier_concerts(concerts, trajets=None):
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
    tries = sorted(candidats, key=lambda c: vers_minutes(c.fin))
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
        score_avec = c.score + (dp[p + 1] if p != -1 else 0.0)
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
        score_avec = c.score + (dp[p + 1] if p != -1 else 0.0)
        score_sans = dp[curr - 1]
        if score_avec > score_sans:
            choisis.append(c)
            curr = p + 1
        else:
            curr = curr - 1

    choisis.reverse()
    return choisis, round(dp[n], 4)