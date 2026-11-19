"""Arbre des genres musicaux (table STYLE_MUSICAL).

L'arbre est un dictionnaire {id_genre: id_parent}. Une racine a pour parent None.
On a seulement besoin de remonter d'un genre vers sa racine : le dictionnaire donne
directement le parent, comme la colonne id_style_parent de la base.
"""


class ArbreGenres:
    def __init__(self):
        self.parent = {}    # id_genre -> id_parent (None si c'est une racine)
        self.libelle = {}   # id_genre -> nom du genre

    def ajouter(self, id_genre, libelle, id_parent=None):
        self.parent[id_genre] = id_parent
        self.libelle[id_genre] = libelle

    def remonter(self, id_genre):
        """Renvoie la liste des (genre, distance), du genre jusqu'à sa racine.

        Le genre lui-même est à distance 0, son parent à 1, son grand-parent à 2...
        Exemple : [(Garage punk, 0), (Garage rock, 1), (Rock, 2)]
        """
        chemin = []
        distance = 0
        # distance <= taille de l'arbre : sécurité au cas où les données auraient une boucle
        while id_genre is not None and distance <= len(self.parent):
            chemin.append((id_genre, distance))
            id_genre = self.parent.get(id_genre)
            distance = distance + 1
        return chemin


def construire_arbre(lignes):
    """Construit l'arbre à partir du résultat de
    SELECT id_style, libelle_style, id_style_parent FROM STYLE_MUSICAL."""
    arbre = ArbreGenres()
    for id_genre, libelle, id_parent in lignes:
        arbre.ajouter(id_genre, libelle, id_parent)
    return arbre
