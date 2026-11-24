from arbre_reel import LIGNES
from profils import ID, creer_arbre

arbre = creer_arbre()


def test_nombre_de_styles_et_de_genres():
    racines = 0
    for id_style, nom, parent in LIGNES:
        if parent is None:
            racines = racines + 1
    assert len(LIGNES) == 273
    assert racines == 13


def test_les_noms_sont_tous_differents():
    # ID associe un nom à un id : deux styles de même nom n'auraient qu'une entrée
    assert len(ID) == 273


def test_chaque_parent_existe():
    ids = []
    for id_style, nom, parent in LIGNES:
        ids.append(id_style)
    for id_style, nom, parent in LIGNES:
        if parent is not None:
            assert parent in ids


def test_chaque_style_arrive_a_une_racine_en_trois_etapes_maximum():
    for id_style, nom, parent in LIGNES:
        chemin = arbre.remonter(id_style)
        assert len(chemin) <= 3
        derniere_etape = chemin[-1][0]
        assert arbre.parent[derniere_etape] is None


def test_exemple_de_la_modelisation():
    # l'exemple de MODELISATION.md : Garage punk -> Garage rock -> Rock
    noms = []
    for genre, distance in arbre.remonter(ID["Garage punk"]):
        noms.append(arbre.libelle[genre])
    assert noms == ["Garage punk", "Garage rock", "Rock"]
