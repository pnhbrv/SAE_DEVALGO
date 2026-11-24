from datetime import datetime
from jeux_essai_planning import PROGRAMMATION_JOURNEE
from modeles import Concert
from planning import planifier_concerts, sont_compatibles, temps_trajet_entre, vers_minutes


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


def test_le_temps_de_trajet_est_respecte():
    # a finit à 20h30 (lieu 1) et c commence à 20h45 (lieu 2) : 15 min pour 30 min de trajet
    a = Concert(id=1, debut=datetime(2026, 7, 10, 20, 0), fin=datetime(2026, 7, 10, 20, 30), score=9.0, lieu=1)
    b = Concert(id=2, debut=datetime(2026, 7, 10, 20, 5), fin=datetime(2026, 7, 10, 20, 40), score=1.0, lieu=2)
    c = Concert(id=3, debut=datetime(2026, 7, 10, 20, 45), fin=datetime(2026, 7, 10, 21, 15), score=5.0, lieu=2)
    selection, score = planifier_concerts([a, b, c], trajets=30)
    assert selection == [a]
    assert score == 9.0


def test_un_seul_concert():
    c1 = Concert(id=1, debut=datetime(2026, 7, 10, 18, 0), fin=datetime(2026, 7, 10, 19, 30), score=4.5)
    selection, score = planifier_concerts([c1])
    assert selection == [c1]
    assert score == 4.5


def test_concerts_dos_a_dos_sans_trajet():
    c1 = Concert(id=1, debut=datetime(2026, 7, 10, 18, 0), fin=datetime(2026, 7, 10, 19, 0), score=3.0, lieu="A")
    c2 = Concert(id=2, debut=datetime(2026, 7, 10, 19, 0), fin=datetime(2026, 7, 10, 20, 0), score=4.0, lieu="B")
    selection, score = planifier_concerts([c1, c2], trajets=0)
    assert selection == [c1, c2]
    assert score == 7.0


def test_trajet_exact_a_la_limite():
    c1 = Concert(id=1, debut=datetime(2026, 7, 10, 16, 0), fin=datetime(2026, 7, 10, 17, 0), score=4.0, lieu="A")
    c2 = Concert(id=2, debut=datetime(2026, 7, 10, 17, 20), fin=datetime(2026, 7, 10, 18, 20), score=5.0, lieu="B")

    selection_ok, score_ok = planifier_concerts([c1, c2], trajets=20)
    assert selection_ok == [c1, c2]
    assert score_ok == 9.0

    selection_ko, score_ko = planifier_concerts([c1, c2], trajets=21)
    assert selection_ko == [c2]
    assert score_ko == 5.0


def test_trajet_ignore_si_lieu_none_ou_trajet_none():
    c1 = Concert(id=1, debut=datetime(2026, 7, 10, 16, 0), fin=datetime(2026, 7, 10, 17, 0), score=4.0, lieu=None)
    c2 = Concert(id=2, debut=datetime(2026, 7, 10, 17, 5), fin=datetime(2026, 7, 10, 18, 0), score=5.0, lieu="B")

    selection_lieu_none, score_lieu_none = planifier_concerts([c1, c2], trajets=30)
    assert selection_lieu_none == [c1, c2]
    assert score_lieu_none == 9.0

    c1.lieu = "A"
    selection_trajet_none, score_trajet_none = planifier_concerts([c1, c2], trajets=None)
    assert selection_trajet_none == [c1, c2]
    assert score_trajet_none == 9.0


def test_tous_les_concerts_en_conflit():
    c1 = Concert(id=1, debut=datetime(2026, 7, 10, 20, 0), fin=datetime(2026, 7, 10, 22, 0), score=2.0)
    c2 = Concert(id=2, debut=datetime(2026, 7, 10, 20, 30), fin=datetime(2026, 7, 10, 21, 30), score=5.0)
    c3 = Concert(id=3, debut=datetime(2026, 7, 10, 21, 0), fin=datetime(2026, 7, 10, 23, 0), score=3.5)
    selection, score = planifier_concerts([c1, c2, c3])
    assert selection == [c2]
    assert score == 5.0


def test_concerts_negatifs_ou_none_ecartes():
    c1 = Concert(id=1, debut=datetime(2026, 7, 10, 15, 0), fin=datetime(2026, 7, 10, 16, 0), score=None)
    c2 = Concert(id=2, debut=datetime(2026, 7, 10, 16, 0), fin=datetime(2026, 7, 10, 17, 0), score=-3.0)
    selection, score = planifier_concerts([c1, c2])
    assert selection == []
    assert score == 0.0


def test_dp_choisit_meme_lieu_compatible_plutot_qu_un_concert_bloque_par_trajet():
    # a (lieu 1) + c (lieu 1) = 7.0, alors que b (lieu 2) vaut 5.0 mais est incompatible avec a et c
    a = Concert(id=1, debut=datetime(2026, 7, 10, 14, 0), fin=datetime(2026, 7, 10, 15, 0), score=4.0, lieu=1)
    b = Concert(id=2, debut=datetime(2026, 7, 10, 15, 5), fin=datetime(2026, 7, 10, 16, 0), score=5.0, lieu=2)
    c = Concert(id=3, debut=datetime(2026, 7, 10, 15, 10), fin=datetime(2026, 7, 10, 16, 10), score=3.0, lieu=1)
    selection, score = planifier_concerts([a, b, c], trajets=20)
    assert selection == [a, c]
    assert score == 7.0


def test_fonctions_utilitaires_planning():
    t1 = datetime(2026, 7, 10, 23, 45)
    t2 = datetime(2026, 7, 11, 0, 15)
    assert vers_minutes(t2, t1) == 30
    assert temps_trajet_entre("Scène A", "Scène A", 15) == 0
    assert temps_trajet_entre("Scène A", "Scène B", 15) == 15
    assert temps_trajet_entre("Scène A", None, 15) == 0

    c1 = Concert(id=1, debut=datetime(2026, 7, 10, 22, 30), fin=t1, lieu="Scène A")
    c2 = Concert(id=2, debut=t2, fin=datetime(2026, 7, 11, 1, 30), lieu="Scène B")
    assert sont_compatibles(c1, c2, trajet=30) is True
    assert sont_compatibles(c1, c2, trajet=31) is False


def test_journee_complete_14h_a_4h_sans_chevauchement():
    concerts = [
        Concert(c.id, c.debut, c.fin, c.genres, score=float((c.id % 5) + 1), lieu=c.lieu)
        for c in PROGRAMMATION_JOURNEE
    ]
    selection, score = planifier_concerts(concerts, trajets=15)
    assert len(selection) > 0
    assert score > 0
    for i in range(len(selection) - 1):
        assert sont_compatibles(selection[i], selection[i + 1], trajet=15)

