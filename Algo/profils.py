"""Profils de festivaliers pour tester le score sur les 273 styles.

Un profil est un dictionnaire {id_style: note}, comme la table PREFERENCE_STYLE.
"""
from arbre_reel import LIGNES
from genres import construire_arbre

# nom du style > son id
ID = {}
for id_style, nom, parent in LIGNES:
    ID[nom] = id_style


def creer_arbre():
    return construire_arbre(LIGNES)


def preferences(notes_par_nom):
    """Écrit un profil avec les noms des styles au lieu des ids.
    Exemple : {"Rock": 5} devient {1: 5} (1 est l'id de Rock)."""
    resultat = {}
    for nom, note in notes_par_nom.items():
        resultat[ID[nom]] = note
    return resultat


# les profils de la base
EMMA = preferences({"Rock": 5, "Garage rock": -3, "Hip-hop": 2})   # le rock sauf le garage rock
LOUIS = preferences({"Électro": 4, "Techno": -4})                  # l'électro mais pas la techno
CHLOE = preferences({"Hip-hop": 5, "Pop": -2})                     # le hip-hop mais pas la pop
THOMAS = preferences({"Punk rock": 5})                             # seulement le punk rock

# cas limites
SANS_PREFERENCE = {}
FAN_DE_TOUT = {}    # +5 sur chacun des 13 genres
REFUSE_TOUT = {}    # -1 sur chacun des 13 genres
for id_style, nom, parent in LIGNES:
    if parent is None:
        FAN_DE_TOUT[id_style] = 5
        REFUSE_TOUT[id_style] = -1
