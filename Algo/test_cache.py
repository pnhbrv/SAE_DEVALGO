from datetime import datetime
from cache import CacheRecommandations, recommander
from jeu_essai import ID, creer_arbre
from modeles import Concert

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
