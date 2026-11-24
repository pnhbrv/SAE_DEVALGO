from datetime import datetime
from modeles import Concert
from planning import planifier_concerts


def test_aucun_concert_a_planifier():
    selection, score = planifier_concerts([])
    assert selection == []
    assert score == 0.0


def test_deux_concerts_sans_conflit_sont_tous_les_deux_gardes():
    c1 = Concert(id=1, debut=datetime(2026, 7, 10, 14, 0), fin=datetime(2026, 7, 10, 15, 30), score=4.0)
    c2 = Concert(id=2, debut=datetime(2026, 7, 10, 16, 0), fin=datetime(2026, 7, 10, 17, 30), score=5.0)
    selection, score = planifier_concerts([c1, c2])
    assert selection == [c1, c2]
    assert score == 9.0


def test_deux_concerts_en_conflit_on_garde_le_meilleur_score():
    c1 = Concert(id=1, debut=datetime(2026, 7, 10, 16, 0), fin=datetime(2026, 7, 10, 18, 0), score=3.0)
    c2 = Concert(id=2, debut=datetime(2026, 7, 10, 16, 30), fin=datetime(2026, 7, 10, 17, 30), score=5.0)
    selection, score = planifier_concerts([c1, c2])
    assert selection == [c2]
    assert score == 5.0


def test_la_programmation_dynamique_bat_l_algo_glouton():
    # c1 (14h-17h, 10) et c3 (18h-21h, 10) rapportent 20 à eux deux
    # un algorithme glouton prendrait c2 (16h-19h, 15) seul
    c1 = Concert(id=1, debut=datetime(2026, 7, 10, 14, 0), fin=datetime(2026, 7, 10, 17, 0), score=10.0)
    c2 = Concert(id=2, debut=datetime(2026, 7, 10, 16, 0), fin=datetime(2026, 7, 10, 19, 0), score=15.0)
    c3 = Concert(id=3, debut=datetime(2026, 7, 10, 18, 0), fin=datetime(2026, 7, 10, 21, 0), score=10.0)
    selection, score = planifier_concerts([c1, c2, c3])
    assert selection == [c1, c3]
    assert score == 20.0


def test_le_passage_de_minuit_sur_deux_jours():
    # Journée du 10 au 11 juillet : 23h00 à 00h30 puis 01h00 à 02h30
    c1 = Concert(id=1, debut=datetime(2026, 7, 10, 23, 0), fin=datetime(2026, 7, 11, 0, 30), score=4.0)
    c2 = Concert(id=2, debut=datetime(2026, 7, 11, 1, 0), fin=datetime(2026, 7, 11, 2, 30), score=5.0)
    selection, score = planifier_concerts([c1, c2])
    assert selection == [c1, c2]
    assert score == 9.0


def test_le_passage_de_minuit_avec_chevauchement():
    # c1 finit le 11 à 01h15 et c2 commence le 11 à 00h45 : vrai chevauchement
    c1 = Concert(id=1, debut=datetime(2026, 7, 10, 23, 30), fin=datetime(2026, 7, 11, 1, 15), score=3.0)
    c2 = Concert(id=2, debut=datetime(2026, 7, 11, 0, 45), fin=datetime(2026, 7, 11, 2, 0), score=4.5)
    selection, score = planifier_concerts([c1, c2])
    assert selection == [c2]
    assert score == 4.5


def test_trajet_entre_deux_lieux_differents():
    # c1 finit à 17h00 sur la Scène A
    c1 = Concert(id=1, debut=datetime(2026, 7, 10, 16, 0), fin=datetime(2026, 7, 10, 17, 0), score=4.0, lieu="Scène A")

    # c2 commence à 17h10 sur Scène B : 10 min d'écart, incompatible avec 20 min de marche
    c2 = Concert(id=2, debut=datetime(2026, 7, 10, 17, 10), fin=datetime(2026, 7, 10, 18, 0), score=5.0, lieu="Scène B")
    selection_incompatible, score_incompatible = planifier_concerts([c1, c2], trajets=20)
    assert selection_incompatible == [c2]
    assert score_incompatible == 5.0

    # c3 commence à 17h30 sur Scène B : 30 min d'écart, compatible avec 20 min de marche
    c3 = Concert(id=3, debut=datetime(2026, 7, 10, 17, 30), fin=datetime(2026, 7, 10, 18, 30), score=5.0, lieu="Scène B")
    selection_compatible, score_compatible = planifier_concerts([c1, c3], trajets=20)
    assert selection_compatible == [c1, c3]
    assert score_compatible == 9.0


def test_trajet_ignore_si_meme_lieu():
    # Deux concerts dans le même lieu avec 5 min d'écart : le trajet de 20 min ne s'applique pas
    c1 = Concert(id=1, debut=datetime(2026, 7, 10, 16, 0), fin=datetime(2026, 7, 10, 17, 0), score=4.0, lieu="Scène A")
    c2 = Concert(id=2, debut=datetime(2026, 7, 10, 17, 5), fin=datetime(2026, 7, 10, 18, 0), score=5.0, lieu="Scène A")
    selection, score = planifier_concerts([c1, c2], trajets=20)
    assert selection == [c1, c2]
    assert score == 9.0


def test_un_concert_sans_score_ou_score_nul_est_ecarte():
    c1 = Concert(id=1, debut=datetime(2026, 7, 10, 15, 0), fin=datetime(2026, 7, 10, 16, 0), score=0.0)
    c2 = Concert(id=2, debut=datetime(2026, 7, 10, 15, 30), fin=datetime(2026, 7, 10, 16, 30), score=3.0)
    selection, score = planifier_concerts([c1, c2])
    assert selection == [c2]
    assert score == 3.0
