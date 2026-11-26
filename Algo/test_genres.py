from genres import ArbreGenres, construire_arbre
from jeu_essai import ID, creer_arbre

arbre = creer_arbre()


def noms_du_chemin(nom_genre):
    """Le chemin vers la racine, avec les noms au lieu des ids."""
    chemin = arbre.remonter(ID[nom_genre])
    return [(arbre.libelle[genre], distance) for genre, distance in chemin]


def test_remonter_jusqu_a_la_racine():
    assert noms_du_chemin("Garage punk") == [("Garage punk", 0), ("Garage rock", 1), ("Rock", 2)]


def test_une_racine_ne_remonte_pas():
    assert noms_du_chemin("Pop") == [("Pop", 0)]


def test_genre_inconnu():
    assert arbre.remonter(999) == [(999, 0)]


def test_boucle_dans_les_donnees():
    # A a pour parent B et B a pour parent A : la remontée doit quand même s'arrêter
    a = ArbreGenres()
    a.ajouter(1, "A", 2)
    a.ajouter(2, "B", 1)
    assert len(a.remonter(1)) <= 3


def test_construire_arbre_comme_le_select_de_la_base():
    lignes = [(1, "Rock", None), (2, "Garage rock", 1), (3, "Garage punk", 2)]
    a = construire_arbre(lignes)
    assert a.parent == {1: None, 2: 1, 3: 2}
    assert a.libelle[3] == "Garage punk"
