from profils import (CHLOE, EMMA, FAN_DE_TOUT, ID, LOUIS, REFUSE_TOUT, SANS_PREFERENCE, THOMAS,
                     creer_arbre, preferences)
from scoring import SCORE_NEUTRE, score_concert, score_genre

arbre = creer_arbre()


def classer(profil, concerts):
    """concerts est une liste de (nom du concert, [ids des genres]).
    Renvoie les (nom, score) du meilleur au moins bon, sans les concerts écartés."""
    resultat = []
    for nom, genres in concerts:
        score = score_concert(arbre, profil, genres)
        if score is not None:
            resultat.append((score, nom))
    resultat.sort(reverse=True)

    classement = []
    for score, nom in resultat:
        classement.append((nom, score))
    return classement


# Emma : le rock, sauf le garage rock

def test_emma_aime_le_rock_et_ses_sous_genres():
    assert score_genre(arbre, EMMA, ID["Rock"]) == 5
    assert round(score_genre(arbre, EMMA, ID["Rock psychédélique"]), 2) == 2.5   # 5 / (1+1)
    assert round(score_genre(arbre, EMMA, ID["Hardcore punk"]), 2) == 1.67       # 5 / (1+2)


def test_emma_refuse_le_garage_rock_et_ses_sous_genres():
    assert score_genre(arbre, EMMA, ID["Garage rock"]) is None
    assert score_genre(arbre, EMMA, ID["Garage revival"]) is None


def test_emma_aime_un_peu_le_hip_hop():
    assert score_genre(arbre, EMMA, ID["Trap"]) == 1                 # 2 / (1+1)
    assert score_genre(arbre, EMMA, ID["Jazz"]) == SCORE_NEUTRE


# Louis : l'électro, mais pas la techno

def test_louis_aime_l_electro_sauf_la_techno():
    assert score_genre(arbre, LOUIS, ID["House"]) == 2               # 4 / (1+1)
    assert round(score_genre(arbre, LOUIS, ID["Deep house"]), 2) == 1.33   # 4 / (1+2)
    assert score_genre(arbre, LOUIS, ID["Techno"]) is None
    assert score_genre(arbre, LOUIS, ID["Minimal techno"]) is None


def test_louis_n_a_pas_de_preference_pour_le_rock():
    assert score_genre(arbre, LOUIS, ID["Rock"]) == SCORE_NEUTRE


# Chloé : le hip-hop, mais pas la pop

def test_chloe_un_seul_genre():
    assert score_genre(arbre, CHLOE, ID["Trap"]) == 2.5              # 5 / (1+1)
    assert score_genre(arbre, CHLOE, ID["K-pop"]) is None


def test_chloe_concert_trap_et_k_pop():
    genres = [ID["Trap"], ID["K-pop"]]
    assert score_concert(arbre, CHLOE, genres) is None
    assert score_concert(arbre, CHLOE, genres, ecarter_si_negatif=False) == 2.5


# Thomas : seulement le punk rock

def test_thomas_aime_le_punk_rock_et_ses_sous_genres():
    assert score_genre(arbre, THOMAS, ID["Punk rock"]) == 5
    assert score_genre(arbre, THOMAS, ID["Pop punk"]) == 2.5         # 5 / (1+1)


def test_thomas_n_aime_pas_le_rock_en_general():
    # la préférence se transmet vers le bas de l'arbre, pas vers le haut
    assert score_genre(arbre, THOMAS, ID["Rock"]) == SCORE_NEUTRE
    assert score_genre(arbre, THOMAS, ID["Folk punk"]) == SCORE_NEUTRE


# cas limites

def test_sans_aucune_preference_tout_est_neutre():
    for nom in ["Rock", "Trap", "Jazz", "Deep house"]:
        assert score_genre(arbre, SANS_PREFERENCE, ID[nom]) == SCORE_NEUTRE


def test_fan_de_tout():
    assert score_genre(arbre, FAN_DE_TOUT, ID["Hip-hop"]) == 5
    assert score_genre(arbre, FAN_DE_TOUT, ID["Trap"]) == 2.5                    # 5 / (1+1)
    assert round(score_genre(arbre, FAN_DE_TOUT, ID["Garage punk"]), 2) == 1.67  # 5 / (1+2)


def test_celui_qui_refuse_tout_n_a_aucun_concert():
    for nom in ["Rock", "Trap", "Jazz", "Deep house", "Chanson bretonne"]:
        assert score_genre(arbre, REFUSE_TOUT, ID[nom]) is None


def test_genre_du_haut_negatif_et_sous_genre_positif():
    profil = preferences({"Rock": -3, "Punk rock": 4})
    assert score_genre(arbre, profil, ID["Punk rock"]) == 4
    assert score_genre(arbre, profil, ID["Pop punk"]) == 2           # 4 / (1+1)
    assert score_genre(arbre, profil, ID["Folk rock"]) is None       # hérite du refus du Rock


def test_genre_inconnu_et_concert_sans_genre():
    assert score_concert(arbre, EMMA, [99999]) == SCORE_NEUTRE
    assert score_concert(arbre, EMMA, []) == SCORE_NEUTRE


def test_plusieurs_genres_max_et_moyenne():
    genres = [ID["Rock psychédélique"], ID["Trap"]]                  # scores 2.5 et 1
    assert score_concert(arbre, EMMA, genres) == 2.5
    assert score_concert(arbre, EMMA, genres, strategie="moyenne") == 1.75


# classement des concerts d'un festivalier

def test_classement_des_concerts_d_emma():
    concerts = [
        ("Concert jazz", [ID["Jazz"]]),
        ("Concert garage", [ID["Garage rock"]]),
        ("Concert rock", [ID["Rock"]]),
        ("Concert trap", [ID["Trap"]]),
    ]
    # le concert de garage rock est écarté
    assert classer(EMMA, concerts) == [("Concert rock", 5), ("Concert trap", 1), ("Concert jazz", 0.05)]
