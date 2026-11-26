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

from .models import EstSimilaire, Evenement, Groupe, PreferenceStyle, StyleMusical

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


def classer_groupes(prefs, nombre, ids_exclus=()):
    """Les groupes du meilleur score au moins bon pour ces préférences.

    Un groupe écarté (style refusé) ou sans rapport avec les préférences (score neutre) n'est pas gardé.
    """
    if len(prefs) == 0:
        return []
    arbre = arbre_des_styles()

    resultats = []
    groupes_par_id = {}
    for unGroupe in Groupe.query.all():
        if unGroupe.id_groupe not in ids_exclus:
            score = score_concert(arbre, prefs, styles_du_groupe(unGroupe))
            if score is not None and score > SCORE_NEUTRE:
                resultats.append((score, unGroupe.id_groupe))
                groupes_par_id[unGroupe.id_groupe] = unGroupe

    # les tuples se trient d'abord sur le score : du meilleur au moins bon
    resultats.sort(reverse=True)

    groupes = []
    for score, id_groupe in resultats[:nombre]:
        groupes.append(groupes_par_id[id_groupe])
    return groupes


def suggestions_groupes(id_spectateur, nombre=6):
    """Les groupes que le spectateur aimera le plus."""
    return classer_groupes(preferences_du_spectateur(id_spectateur), nombre)


def groupes_similaires(unGroupe, nombre=4):
    """Les groupes proches de celui-ci.

    D'abord ceux que l'organisateur a déclarés similaires (table EST_SIMILAIRE), puis on complète avec
    l'algo : on fait comme si un spectateur aimait (+5) les styles du groupe, et on garde ses meilleures
    suggestions. Un groupe d'un sous-genre voisin arrive donc avant un groupe d'un autre genre.
    """
    similaires = []
    ids_deja_pris = [unGroupe.id_groupe]
    for unLien in EstSimilaire.query.filter_by(id_groupe=unGroupe.id_groupe).all():
        unSimilaire = Groupe.query.filter_by(id_groupe=unLien.id_groupe_similaire).first()
        if unSimilaire is not None and len(similaires) < nombre:
            similaires.append(unSimilaire)
            ids_deja_pris.append(unSimilaire.id_groupe)

    prefs = {}
    for id_style in styles_du_groupe(unGroupe):
        prefs[id_style] = 5
    for unProche in classer_groupes(prefs, nombre - len(similaires), ids_deja_pris):
        similaires.append(unProche)
    return similaires


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
