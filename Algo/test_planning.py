from datetime import datetime
from modeles import Concert
from planning import planifier_concerts


def test_aucun_concert_a_planifier():
    selection, score = planifier_concerts([])
    assert selection == []
    assert score == 0.0


def test_deux_concerts_sans_conflit_sont_tous_les_deux_gardes():
    c1 = Concert(id=1, debut="14:00", fin="15:30", score=4.0)
    c2 = Concert(id=2, debut="16:00", fin="17:30", score=5.0)
    selection, score = planifier_concerts([c1, c2])
    assert selection == [c1, c2]
    assert score == 9.0


def test_deux_concerts_en_conflit_on_garde_le_meilleur_score():
    c1 = Concert(id=1, debut="16:00", fin="18:00", score=3.0)
    c2 = Concert(id=2, debut="16:30", fin="17:30", score=5.0)
    selection, score = planifier_concerts([c1, c2])
    assert selection == [c2]
    assert score == 5.0


def test_la_programmation_dynamique_bat_l_algo_glouton():
    # c1 (14h-17h, 10) et c3 (18h-21h, 10) rapportent 20 à eux deux
    # un glouton prendrait c2 (16h-19h, 15) seul
    c1 = Concert(id=1, debut="14:00", fin="17:00", score=10.0)
    c2 = Concert(id=2, debut="16:00", fin="19:00", score=15.0)
    c3 = Concert(id=3, debut="18:00", fin="21:00", score=10.0)
    selection, score = planifier_concerts([c1, c2, c3])
    assert selection == [c1, c3]
    assert score == 20.0


def test_le_passage_de_minuit_sans_conflit():
    # 23h00 à 00h30 puis 01h00 à 02h30 : pas de chevauchement malgré le changement de jour
    c1 = Concert(id=1, debut="23:00", fin="00:30", score=4.0)
    c2 = Concert(id=2, debut="01:00", fin="02:30", score=5.0)
    selection, score = planifier_concerts([c1, c2])
    assert selection == [c1, c2]
    assert score == 9.0


def test_le_passage_de_minuit_avec_chevauchement():
    # c1 finit à 01h15 et c2 commence à 00h45 : vrai chevauchement
    c1 = Concert(id=1, debut="23:30", fin="01:15", score=3.0)
    c2 = Concert(id=2, debut="00:45", fin="02:00", score=4.5)
    selection, score = planifier_concerts([c1, c2])
    assert selection == [c2]
    assert score == 4.5


def test_le_temps_de_trajet_rend_deux_concerts_incompatibles():
    # 17h00 à 17h10 : 10 min d'écart, mais 20 min de marche entre Scène A et Scène B
    c1 = Concert(id=1, debut="16:00", fin="17:00", score=4.0, lieu="Scène A")
    c2 = Concert(id=2, debut="17:10", fin="18:00", score=5.0, lieu="Scène B")

    # sans trajet, ils sont compatibles
    sel, score = planifier_concerts([c1, c2])
    assert sel == [c1, c2]

    # avec 20 min de trajet, on doit choisir le meilleur
    trajets = {("Scène A", "Scène B"): 20}
    sel, score = planifier_concerts([c1, c2], trajets=trajets)
    assert sel == [c2]
    assert score == 5.0


def test_un_concert_sans_score_ou_score_nul_est_ecarte():
    c1 = Concert(id=1, debut="15:00", fin="16:00", score=0.0)
    c2 = Concert(id=2, debut="15:30", fin="16:30", score=3.0)
    selection, score = planifier_concerts([c1, c2])
    assert selection == [c2]
    assert score == 3.0


def test_avec_objets_datetime_complets():
    d1 = datetime(2026, 7, 10, 22, 0)
    f1 = datetime(2026, 7, 10, 23, 30)
    d2 = datetime(2026, 7, 11, 0, 15)
    f2 = datetime(2026, 7, 11, 1, 45)

    c1 = Concert(id=1, debut=d1, fin=f1, score=4.0)
    c2 = Concert(id=2, debut=d2, fin=f2, score=4.0)
    selection, score = planifier_concerts([c1, c2])
    assert selection == [c1, c2]
    assert score == 8.0