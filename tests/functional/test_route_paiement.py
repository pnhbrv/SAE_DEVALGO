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


def test_paiement_demande_connexion(client):
    response = client.get('/paiement/?id_type_billet=1', follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/connexion/"
    assert "Veuillez vous connecter pour accéder au paiement.".encode() in response.data
    assert b'value="/paiement/?id_type_billet=1"' in response.data


def test_paiement_affiche_pass_selectionnes_et_total(client, testapp):
    with testapp.app_context():
        db.session.add_all([
            TypeBillet(libelle="Pass 1 jour", prix=35.00),
            TypeBillet(libelle="Pass étudiant", prix=25.00),
        ])
        db.session.commit()

    connecter_spectateur(client, testapp)
    response = client.get('/paiement/?id_type_billet=1&id_type_billet=2')

    assert response.status_code == 200
    assert "Pass 1 jour".encode() in response.data
    assert "Pass étudiant".encode() in response.data
    assert "60.00€".encode() in response.data
    assert b'Paiement</a>' not in response.data
    assert "Le paiement sera activé après l’intégration".encode() in response.data


def test_paiement_sans_pass_affiche_message_de_liaison(client, testapp):
    connecter_spectateur(client, testapp)
    response = client.get('/paiement/')

    assert response.status_code == 200
    assert "Mon espace sera relié à cette page.".encode() in response.data
    assert b'<button class="paiement-total" type="button" disabled>' in response.data


def test_paiement_refuse_un_pass_indisponible(client, testapp):
    connecter_spectateur(client, testapp)
    response = client.get('/paiement/?id_type_billet=999')

    assert response.status_code == 200
    assert "Un ou plusieurs billets ne sont plus disponibles.".encode() in response.data
