"""Arbre simple créé uniquement pour tests"""
from genres import ArbreGenres

# (nom du genre, nom de son parent)
GENRES = [
    ("Rock", None),
    ("Folk rock", "Rock"), ("Folk punk", "Folk rock"),
    ("Garage rock", "Rock"), ("Garage punk", "Garage rock"),
    ("Punk rock", "Rock"), ("Hardcore punk", "Punk rock"), ("Pop punk", "Punk rock"),
    ("Hip-hop", None),
    ("Trap", "Hip-hop"), ("Cloud rap", "Trap"), ("Drill", "Hip-hop"),
    ("Électro", None),
    ("Techno", "Électro"), ("Minimal techno", "Techno"),
    ("House", "Électro"), ("Deep house", "House"),
    ("Pop", None), ("Synth-pop", "Pop"), ("New wave", "Synth-pop"),
]

# nom du genre -> son id (1, 2, 3... dans l'ordre de la liste)
ID = {}
numero = 1
for nom, parent in GENRES:
    ID[nom] = numero
    numero = numero + 1


def creer_arbre():
    arbre = ArbreGenres()
    for nom, parent in GENRES:
        if parent is None:
            arbre.ajouter(ID[nom], nom)
        else:
            arbre.ajouter(ID[nom], nom, ID[parent])
    return arbre
