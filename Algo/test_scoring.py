from jeu_essai import ID, creer_arbre
from scoring import SCORE_NEUTRE, score_concert, score_genre

arbre = creer_arbre()


# un seul genre (1.3)

def test_preference_directe():
    prefs = {ID["Rock"]: 5}
    assert score_genre(arbre, prefs, ID["Rock"]) == 5


def test_preference_heritee_du_parent():
    prefs = {ID["Rock"]: 5}
    assert round(score_genre(arbre, prefs, ID["Folk rock"]), 2) == 2.5    # 5 / (1+1)
    assert round(score_genre(arbre, prefs, ID["Folk punk"]), 2) == 1.67   # 5 / (1+2)


def test_le_rock_sauf_le_garage_rock():
    prefs = {ID["Rock"]: 5, ID["Garage rock"]: -3}
    assert round(score_genre(arbre, prefs, ID["Punk rock"]), 2) == 2.5
    assert score_genre(arbre, prefs, ID["Garage rock"]) is None
    # Garage punk est un sous-genre de Garage rock : il hérite du refus
    assert score_genre(arbre, prefs, ID["Garage punk"]) is None


def test_la_preference_la_plus_proche_gagne():
    prefs = {ID["Rock"]: -2, ID["Punk rock"]: 4}
    assert score_genre(arbre, prefs, ID["Punk rock"]) == 4
    assert score_genre(arbre, prefs, ID["Pop punk"]) == 2          # 4 / (1+1)
    assert score_genre(arbre, prefs, ID["Folk rock"]) is None      # hérite de Rock = -2


def test_une_preference_negative_ecarte_tout_le_sous_arbre():
    prefs = {ID["Électro"]: -4}
    for nom in ["Électro", "Techno", "Minimal techno", "House", "Deep house"]:
        assert score_genre(arbre, prefs, ID[nom]) is None


def test_aucune_preference_donne_le_score_neutre():
    assert score_genre(arbre, {ID["Rock"]: 5}, ID["Pop"]) == SCORE_NEUTRE
    assert score_genre(arbre, {}, ID["Rock"]) == SCORE_NEUTRE


def test_le_score_neutre_est_plus_petit_qu_une_vraie_preference():
    prefs = {ID["Rock"]: 1}   # la plus petite note positive
    assert score_genre(arbre, prefs, ID["Folk punk"]) > SCORE_NEUTRE   # 1/3 > 0.05


def test_un_genre_proche_passe_avant_un_genre_lointain():
    prefs = {ID["Hip-hop"]: 5}
    assert score_genre(arbre, prefs, ID["Trap"]) > score_genre(arbre, prefs, ID["Cloud rap"])


def test_genre_inconnu_donne_le_score_neutre():
    assert score_genre(arbre, {ID["Rock"]: 5}, 999) == SCORE_NEUTRE


# plusieurs genres (1.4)

def test_un_genre_negatif_ecarte_le_concert():
    prefs = {ID["Rock"]: 5, ID["Garage rock"]: -3}
    genres = [ID["Punk rock"], ID["Garage rock"]]
    assert score_concert(arbre, prefs, genres) is None


def test_sans_ecarter_on_garde_les_genres_acceptes():
    prefs = {ID["Rock"]: 5, ID["Garage rock"]: -3}
    genres = [ID["Punk rock"], ID["Garage rock"]]
    assert score_concert(arbre, prefs, genres, ecarter_si_negatif=False) == 2.5


def test_tous_les_genres_negatifs():
    prefs = {ID["Électro"]: -4}
    genres = [ID["Techno"], ID["House"]]
    assert score_concert(arbre, prefs, genres, ecarter_si_negatif=False) is None


def test_strategie_max():
    prefs = {ID["Rock"]: 5}
    genres = [ID["Rock"], ID["Punk rock"]]    # scores 5 et 2.5
    assert score_concert(arbre, prefs, genres, "max") == 5


def test_strategie_moyenne():
    prefs = {ID["Rock"]: 5}
    genres = [ID["Rock"], ID["Punk rock"]]
    assert score_concert(arbre, prefs, genres, "moyenne") == 3.75


def test_concert_sans_genre():
    assert score_concert(arbre, {}, []) == SCORE_NEUTRE


def test_fan_de_hip_hop_qui_n_aime_pas_la_pop():
    prefs = {ID["Hip-hop"]: 5, ID["Pop"]: -2}
    assert score_concert(arbre, prefs, [ID["Trap"]]) == 2.5
    assert score_concert(arbre, prefs, [ID["Trap"], ID["Synth-pop"]]) is None
    assert score_concert(arbre, prefs, [ID["Trap"], ID["Synth-pop"]], ecarter_si_negatif=False) == 2.5
