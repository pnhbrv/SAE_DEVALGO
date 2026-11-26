"""Lien entre le site et la partie Algo : on lit la base, puis on appelle les fonctions de Algo/."""
import os
import sys
from datetime import timedelta

# Algo/ n'est pas un paquet Python : on ajoute le dossier au chemin pour importer ses modules
DOSSIER_ALGO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Algo")
if DOSSIER_ALGO not in sys.path:
    sys.path.append(DOSSIER_ALGO)

from cache import CacheRecommandations, recommander
from genres import construire_arbre
from modeles import Concert
from scoring import SCORE_NEUTRE, score_concert

from .models import Evenement, Groupe, PreferenceStyle, StyleMusical

# temps (en minutes) pour aller d'un lieu du festival à un autre
TEMPS_TRAJET = 15

# la programmation n'a pas de numéro de version dans la base du site : le cache d'un spectateur
# est vidé quand il change ses préférences (voir preference/routes.py)
VERSION_PROGRAMMATION = 1

cache = CacheRecommandations()


def arbre_des_styles():
    lignes = []
    for unStyle in StyleMusical.query.all():
        lignes.append((unStyle.id_style, unStyle.libelle_style, unStyle.id_style_parent))
    return construire_arbre(lignes)


def preferences_du_spectateur(id_spectateur):
    """Renvoie {id_style: note}, le format attendu par scoring.py."""
    prefs = {}
    for unePreference in PreferenceStyle.query.filter_by(id_spectateur=id_spectateur).all():
        prefs[unePreference.id_style] = unePreference.note
    return prefs


def styles_du_groupe(unGroupe):
    ids = []
    for unLien in unGroupe.styles:
        ids.append(unLien.id_style)
    return ids


def suggestions_groupes(id_spectateur, nombre=6):
    """Les groupes que le spectateur aimera le plus, du meilleur score au moins bon.

    Un groupe écarté (style refusé) ou sans rapport avec ses goûts (score neutre) n'est pas proposé.
    """
    prefs = preferences_du_spectateur(id_spectateur)
    if len(prefs) == 0:
        return []
    arbre = arbre_des_styles()

    resultats = []
    groupes_par_id = {}
    for unGroupe in Groupe.query.all():
        score = score_concert(arbre, prefs, styles_du_groupe(unGroupe))
        if score is not None and score > SCORE_NEUTRE:
            resultats.append((score, unGroupe.id_groupe))
            groupes_par_id[unGroupe.id_groupe] = unGroupe

    # les tuples se trient d'abord sur le score : du meilleur au moins bon
    resultats.sort(reverse=True)

    suggestions = []
    for score, id_groupe in resultats[:nombre]:
        suggestions.append(groupes_par_id[id_groupe])
    return suggestions


def concert_depuis_evenement(unEvenement):
    """Transforme un EVENEMENT de la base en Concert de Algo/modeles.py."""
    genres = []
    for uneParticipation in unEvenement.participations:
        for id_style in styles_du_groupe(uneParticipation.groupe):
            if id_style not in genres:
                genres.append(id_style)
    # la fin ne compte pas le démontage : le spectateur peut partir dès la fin du concert
    fin = unEvenement.date_heure_debut + timedelta(minutes=unEvenement.duree)
    return Concert(unEvenement.id_evenement, unEvenement.date_heure_debut, fin, genres, lieu=unEvenement.id_lieu)


def concerts_conseilles(id_spectateur):
    """Le planning conseillé : les concerts qui ne se chevauchent pas avec le meilleur score total.

    Renvoie la liste des Evenement, dans l'ordre chronologique, et le score total.
    """
    if cache.est_valide(id_spectateur, VERSION_PROGRAMMATION):
        # résultat déjà calculé : on évite même de relire la programmation dans la base
        selection, score_total = cache.obtenir(id_spectateur)
    else:
        prefs = preferences_du_spectateur(id_spectateur)
        if len(prefs) == 0:
            return [], 0.0
        concerts = []
        for unEvenement in Evenement.query.filter_by(type_evenement="Concert", est_public=True).all():
            concerts.append(concert_depuis_evenement(unEvenement))
        selection, score_total = recommander(id_spectateur, arbre_des_styles(), prefs, concerts, cache=cache,
                                             version_prog=VERSION_PROGRAMMATION, trajets=TEMPS_TRAJET)

    evenements = []
    for unConcert in selection:
        evenements.append(Evenement.query.filter_by(id_evenement=unConcert.id).first())
    return evenements, score_total
