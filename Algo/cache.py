"""Évite de recalculer le score et le planning pour un festivalier si :
- la programmation n'a pas changé (numéro de version identique)
- les préférences du festivalier n'ont pas changé depuis le dernier calcul
"""
import time
from modeles import Concert
from planning import planifier_concerts
from scoring import score_concert


class CacheRecommandations:
    def __init__(self):
        # id_spectateur -> dict avec :
        #   version_prog : version de la programmation lors du calcul
        #   date_prefs   : date/version des préférences du spectateur
        #   date_calcul  : timestamp du calcul
        #   concerts     : liste des concerts recommandés
        #   score_total  : score cumulé
        self.entrees = {}

    def est_valide(self, id_spectateur, version_prog_actuelle, date_prefs_actuelle=None):
        """Vérifie si le cache est présent et toujours à jour."""
        if id_spectateur not in self.entrees:
            return False

        entree = self.entrees[id_spectateur]

        # la programmation du festival a changé (ex: concert ajouté/annulé)
        if entree["version_prog"] != version_prog_actuelle:
            return False

        # le festivalier a modifié ses préférences après le dernier calcul
        if date_prefs_actuelle is not None:
            if entree["date_prefs"] is None or entree["date_prefs"] < date_prefs_actuelle:
                return False

        return True

    def obtenir(self, id_spectateur):
        """Renvoie (concerts, score_total) depuis le cache, ou None si absent."""
        if id_spectateur not in self.entrees:
            return None
        entree = self.entrees[id_spectateur]
        return entree["concerts"], entree["score_total"]

    def enregistrer(self, id_spectateur, concerts, score_total, version_prog, date_prefs=None):
        """Sauvegarde le résultat d'un calcul de recommandation."""
        self.entrees[id_spectateur] = {
            "version_prog": version_prog,
            "date_prefs": date_prefs,
            "date_calcul": time.time(),
            "concerts": concerts,
            "score_total": score_total,
        }

    def invalider(self, id_spectateur=None):
        """Vide le cache pour un spectateur, ou pour tout le monde si None."""
        if id_spectateur is None:
            self.entrees.clear()
        elif id_spectateur in self.entrees:
            del self.entrees[id_spectateur]


def recommander(id_spectateur, arbre, prefs, tous_les_concerts,
                cache=None, version_prog=1, date_prefs=None, trajets=None,
                strategie="max", ecarter_si_negatif=True):
    """Fonction principale de recommandation pour un festivalier.

    1. Regarde d'abord dans le cache
    2. Si le cache est périmé ou absent :
       - calcule le score de chaque concert selon les préférences
       - sélectionne le planning optimal sans chevauchement (DP)
       - met en cache le résultat
    3. Renvoie (concerts_recommandes, score_total)
    """
    # 1. vérification du cache
    if cache is not None and cache.est_valide(id_spectateur, version_prog, date_prefs):
        return cache.obtenir(id_spectateur)

    # 2. calcul des scores pour ce festivalier
    candidats = []
    for c in tous_les_concerts:
        score = score_concert(arbre, prefs, c.genres,
                              strategie=strategie,
                              ecarter_si_negatif=ecarter_si_negatif)
        if score is not None and score > 0:
            # copie légère du concert avec le score calculé pour ce spectateur
            candidat = Concert(c.id, c.debut, c.fin, c.genres, score=score, lieu=c.lieu)
            candidats.append(candidat)

    # 3. sélection optimale sans chevauchement (Weighted Interval Scheduling)
    selection, score_total = planifier_concerts(candidats, trajets=trajets)

    # 4. mise à jour du cache
    if cache is not None:
        cache.enregistrer(id_spectateur, selection, score_total, version_prog, date_prefs)

    return selection, score_total
