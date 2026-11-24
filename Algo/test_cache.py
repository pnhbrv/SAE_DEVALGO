from datetime import datetime
from cache import CacheRecommandations, recommander
from jeu_essai import ID, creer_arbre
from jeux_essai_planning import (
    PROGRAMMATION_JOURNEE,
    PROFIL_ELECTRO,
    PROFIL_FAN_DE_TOUT,
    PROFIL_RAP,
    PROFIL_REFUSE_TOUT,
    PROFIL_ROCK,
    PROFIL_SANS_PREFERENCE,
)
from modeles import Concert
from planning import sont_compatibles

arbre = creer_arbre()

# programmation d'essai
CONCERTS = [
    Concert(id=1, debut=datetime(2026, 7, 10, 16, 0), fin=datetime(2026, 7, 10, 17, 30), genres=[ID["Rock"]]),
    Concert(id=2, debut=datetime(2026, 7, 10, 17, 0), fin=datetime(2026, 7, 10, 18, 30), genres=[ID["Hip-hop"]]),
    Concert(id=3, debut=datetime(2026, 7, 10, 19, 0), fin=datetime(2026, 7, 10, 20, 30), genres=[ID["Techno"]]),
]



def test_le_cache_renvoie_directement_sans_recalculer():
    cache = CacheRecommandations()
    prefs = {ID["Rock"]: 5}

    # premier appel : calcul et mise en cache
    res1, score1 = recommander(1, arbre, prefs, CONCERTS, cache=cache, version_prog=1)

    assert cache.est_valide(1, version_prog_actuelle=1)
    res_cache, score_cache = cache.obtenir(1)
    assert res_cache == res1
    assert score_cache == score1

    # deuxième appel : doit renvoyer exactement le même résultat issu du cache
    res2, score2 = recommander(1, arbre, prefs, CONCERTS, cache=cache, version_prog=1)
    assert res2 == res1
    assert score2 == score1


def test_le_cache_est_invalide_si_la_programmation_change():
    cache = CacheRecommandations()
    prefs = {ID["Rock"]: 5}

    # calcul avec la version 1 de la programmation
    recommander(1, arbre, prefs, CONCERTS, cache=cache, version_prog=1)
    assert cache.est_valide(1, version_prog_actuelle=1) is True

    # la programmation passe en version 2 (organisateur a modifié un concert)
    assert cache.est_valide(1, version_prog_actuelle=2) is False


def test_le_cache_est_invalide_si_les_preferences_changent():
    cache = CacheRecommandations()
    prefs_v1 = {ID["Rock"]: 5}

    # calcul avec les préférences datées de 100
    recommander(1, arbre, prefs_v1, CONCERTS, cache=cache, version_prog=1, date_prefs=100)
    assert cache.est_valide(1, version_prog_actuelle=1, date_prefs_actuelle=100) is True

    # le festivalier modifie ses préférences à la date 150 : le cache est périmé
    assert cache.est_valide(1, version_prog_actuelle=1, date_prefs_actuelle=150) is False


def test_invalidation_manuelle_du_cache():
    cache = CacheRecommandations()
    prefs = {ID["Rock"]: 5}

    recommander(1, arbre, prefs, CONCERTS, cache=cache, version_prog=1)
    recommander(2, arbre, prefs, CONCERTS, cache=cache, version_prog=1)

    # invalider uniquement le spectateur 1
    cache.invalider(1)
    assert cache.obtenir(1) is None
    assert cache.obtenir(2) is not None

    # invalider tout le monde
    cache.invalider()
    assert cache.obtenir(2) is None


def test_recommander_fonctionne_sans_cache():
    prefs = {ID["Rock"]: 5}
    res, score = recommander(1, arbre, prefs, CONCERTS, cache=None)
    assert len(res) > 0
    assert score > 0


def test_deux_spectateurs_ont_chacun_leur_recommandation():
    cache = CacheRecommandations()
    prefs_rock = {ID["Rock"]: 5, ID["Hip-hop"]: -5}
    prefs_rap = {ID["Hip-hop"]: 5, ID["Rock"]: -5}

    # spectateur 1 aime le rock
    res1, _ = recommander(1, arbre, prefs_rock, CONCERTS, cache=cache)
    # spectateur 2 aime le rap
    res2, _ = recommander(2, arbre, prefs_rap, CONCERTS, cache=cache)

    assert any(c.id == 1 for c in res1)
    assert all(c.id != 2 for c in res1)

    assert any(c.id == 2 for c in res2)
    assert all(c.id != 1 for c in res2)


def test_le_cache_evite_vraiment_le_recalcul():
    cache = CacheRecommandations()
    prefs = {ID["Rock"]: 5}

    res1, score1 = recommander(1, arbre, prefs, CONCERTS, cache=cache, version_prog=1)
    date_calcul_initiale = cache.entrees[1]["date_calcul"]

    # On passe une liste vide tout en gardant la même version_prog :
    # si le cache est bien utilisé, on récupère l'ancien résultat sans recalculer.
    res2, score2 = recommander(1, arbre, prefs, [], cache=cache, version_prog=1)
    assert res2 == res1
    assert score2 == score1
    assert cache.entrees[1]["date_calcul"] == date_calcul_initiale


def test_cache_avec_resultat_vide():
    cache = CacheRecommandations()
    res, score = recommander(
        1, arbre, PROFIL_REFUSE_TOUT, PROGRAMMATION_JOURNEE, cache=cache, version_prog=1
    )
    assert res == []
    assert score == 0.0
    assert cache.est_valide(1, version_prog_actuelle=1) is True
    assert cache.obtenir(1) == ([], 0.0)


def test_cache_date_prefs_cas_limites():
    cache = CacheRecommandations()
    prefs = {ID["Rock"]: 5}

    # Cache sans date_prefs : si une date actuelle est fournie ensuite, il est périmé
    recommander(1, arbre, prefs, CONCERTS, cache=cache, version_prog=1, date_prefs=None)
    assert cache.est_valide(1, version_prog_actuelle=1, date_prefs_actuelle=100) is False

    # Cache daté à 100 : valide pour <= 100 ou None, périmé pour > 100
    recommander(1, arbre, prefs, CONCERTS, cache=cache, version_prog=1, date_prefs=100)
    assert cache.est_valide(1, version_prog_actuelle=1, date_prefs_actuelle=None) is True
    assert cache.est_valide(1, version_prog_actuelle=1, date_prefs_actuelle=90) is True
    assert cache.est_valide(1, version_prog_actuelle=1, date_prefs_actuelle=100) is True
    assert cache.est_valide(1, version_prog_actuelle=1, date_prefs_actuelle=101) is False


def test_invalider_spectateur_inconnu_ne_plante_pas():
    cache = CacheRecommandations()
    cache.invalider(999)
    assert cache.obtenir(999) is None


def test_recommander_journee_realiste_plusieurs_profils():
    cache = CacheRecommandations()

    # Profil Rock (sauf Garage rock) avec 15 min de trajet entre scènes
    res_rock, score_rock = recommander(
        1, arbre, PROFIL_ROCK, PROGRAMMATION_JOURNEE, cache=cache, version_prog=1, trajets=15
    )
    ids_rock = {c.id for c in res_rock}
    assert 5 not in ids_rock   # Rock + Garage rock -> écarté par défaut
    assert 15 not in ids_rock  # Garage punk -> hérite de Garage rock (-3) -> écarté
    assert score_rock > 0
    for i in range(len(res_rock) - 1):
        assert sont_compatibles(res_rock[i], res_rock[i + 1], trajet=15)

    # Sans écarter sur un genre négatif, le concert 5 devient candidat
    res_rock_souple, _ = recommander(
        2, arbre, PROFIL_ROCK, PROGRAMMATION_JOURNEE, ecarter_si_negatif=False, trajets=15
    )
    assert any(c.id == 5 for c in res_rock_souple)

    # Profil Électro (sauf Techno)
    res_electro, _ = recommander(
        3, arbre, PROFIL_ELECTRO, PROGRAMMATION_JOURNEE, cache=cache, version_prog=1, trajets=15
    )
    ids_electro = {c.id for c in res_electro}
    assert 12 not in ids_electro  # Techno / Minimal techno -> écarté
    assert 14 in ids_electro      # House / Deep house après minuit
    assert 16 in ids_electro      # Électro / House jusqu'à 4h

    # Profil Rap (sauf Pop)
    res_rap, _ = recommander(
        4, arbre, PROFIL_RAP, PROGRAMMATION_JOURNEE, cache=cache, version_prog=1, trajets=15
    )
    ids_rap = {c.id for c in res_rap}
    assert 2 not in ids_rap   # Pop / Synth-pop -> écarté
    assert 9 not in ids_rap   # New wave / Synth-pop -> écarté
    assert 13 in ids_rap      # Hip-hop / Cloud rap après minuit

    # Profil sans préférence : propose un planning complet avec score neutre (0.05 par concert)
    res_neutre, score_neutre = recommander(
        5, arbre, PROFIL_SANS_PREFERENCE, PROGRAMMATION_JOURNEE, trajets=15
    )
    assert len(res_neutre) > 0
    assert score_neutre == round(0.05 * len(res_neutre), 4)

    # Fan de tout vs Refuse tout
    _, score_fan = recommander(6, arbre, PROFIL_FAN_DE_TOUT, PROGRAMMATION_JOURNEE, trajets=15)
    res_refus, score_refus = recommander(7, arbre, PROFIL_REFUSE_TOUT, PROGRAMMATION_JOURNEE, trajets=15)
    assert score_fan > score_neutre
    assert res_refus == []
    assert score_refus == 0.0

