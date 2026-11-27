# Tests de la page de billetterie [Source : TP 1 — test_index ; TP 5 — tests des routes ; maquette billetterie]
from monApp.app import db
from monApp.commands import hacher
from monApp.models import Spectateur, TypeBillet
from tests.functional import login


def connecter_spectateur(client, testapp):
    with testapp.app_context():
        db.session.add(Spectateur(
            nom="Dubois",
            prenom="Jean",
            email="jean@mail.com",
            mot_de_passe=hacher("jean"),
        ))
        db.session.commit()
    login(client, "jean@mail.com", "jean", "")


def test_billeterie_demande_connexion(client):
    response = client.get('/billeterie/', follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/connexion/"
    assert "Veuillez vous connecter pour accéder à la billetterie.".encode() in response.data


def test_billeterie_get_defaut(client, testapp):
    connecter_spectateur(client, testapp)
    response = client.get('/billeterie/')
    assert response.status_code == 200
    assert "Billeterie".encode() in response.data
    assert "Voici les formules disponibles !".encode() in response.data
    assert "Pass 1 jour".encode() in response.data
    assert "Pass 2 jours".encode() in response.data
    assert "Pass étudiant".encode() in response.data
    assert "Pass tout festival".encode() in response.data
    assert "35.00€*".encode() in response.data
    assert "60.00€*".encode() in response.data
    assert "25.00€*".encode() in response.data
    assert "120.00€*".encode() in response.data
    assert "Sélectionner".encode() in response.data
    assert "*Accès aux Événements payants".encode() in response.data
    assert b'href="/billeterie/"' in response.data
    assert "Confirmer mon choix".encode() not in response.data
    assert "Evenements".encode() in response.data
    assert "Programmation".encode() in response.data
    assert "Artiste".encode() in response.data
    assert "Mon espace".encode() in response.data


def test_billeterie_avec_bdd(client, testapp):
    with testapp.app_context():
        db.session.add(TypeBillet(libelle="Pass 1 jour", prix=19.99))
        db.session.add(TypeBillet(libelle="Pass VIP", prix=99.99))
        db.session.commit()

    connecter_spectateur(client, testapp)
    response = client.get('/billeterie/')
    assert response.status_code == 200
    assert "Pass 1 jour".encode() in response.data
    assert "Pass VIP".encode() in response.data
    assert "99.99€*".encode() in response.data


def test_billetterie_alias(client, testapp):
    connecter_spectateur(client, testapp)
    response = client.get('/billetterie/')
    assert response.status_code == 200
    assert "Billeterie".encode() in response.data


def test_selectionner_non_connecte(client):
    response = client.get('/billeterie/selection/1/', follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/connexion/"
    assert "Veuillez vous connecter pour réserver votre billet.".encode() in response.data
    assert b'value="/billeterie/selection/1/"' in response.data


def test_selectionner_connecte(client, testapp):
    with testapp.app_context():
        t = TypeBillet(libelle="Pass 1 jour", prix=19.99)
        db.session.add(t)
        db.session.commit()
        id_billet = t.id_type_billet

    connecter_spectateur(client, testapp)
    response = client.get(f'/billeterie/selection/{id_billet}/', follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/billeterie/"
    assert "Vous avez sélectionné : Pass 1 jour.".encode() in response.data
    assert b"carte-billet-selectionnee" in response.data
    assert "Désélectionner".encode() in response.data
    assert "Confirmer mon choix".encode() in response.data
    assert b'href="/paiement/"' in response.data


def test_selectionner_pass_selectionne_peut_etre_retire(client, testapp):
    with testapp.app_context():
        db.session.add(TypeBillet(libelle="Pass 1 jour", prix=19.99))
        db.session.commit()

    connecter_spectateur(client, testapp)
    client.get('/billeterie/selection/1/')
    response = client.get('/billeterie/selection/1/', follow_redirects=True)

    assert response.status_code == 200
    assert "Vous avez retiré : Pass 1 jour.".encode() in response.data
    assert b"carte-billet-selectionnee" not in response.data


def test_selectionner_billet_inconnu(client, testapp):
    connecter_spectateur(client, testapp)
    response = client.get('/billeterie/selection/999/', follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/billeterie/"
    assert b"pas disponible." in response.data


def test_selectionner_formule_de_demo_sans_bdd(client, testapp):
    connecter_spectateur(client, testapp)
    response = client.get('/billeterie/selection/1/', follow_redirects=True)
    assert response.status_code == 200
    assert "Vous avez sélectionné : Pass 1 jour.".encode() in response.data


def test_selectionner_quantite_via_popup(client, testapp):
    with testapp.app_context():
        db.session.add(TypeBillet(libelle="Pass 1 jour", prix=19.99))
        db.session.commit()

    connecter_spectateur(client, testapp)
    response = client.post('/billeterie/selection/1/', data={"quantite": "3"}, follow_redirects=True)
    assert response.status_code == 200
    assert "Quantité sélectionnée pour Pass 1 jour : 3.".encode() in response.data
    assert "Pass sélectionné (x3)".encode() in response.data
    assert b"quantite-stepper" in response.data

    response = client.post('/billeterie/selection/1/', data={"quantite": "0"}, follow_redirects=True)
    assert response.status_code == 200
    assert "Vous avez retiré : Pass 1 jour.".encode() in response.data
    assert b"carte-billet-selectionnee" not in response.data


def test_selectionner_quantite_invalide(client, testapp):
    connecter_spectateur(client, testapp)
    response = client.post('/billeterie/selection/1/', data={"quantite": "abc"}, follow_redirects=True)
    assert response.status_code == 200
    assert "Quantité invalide.".encode() in response.data
