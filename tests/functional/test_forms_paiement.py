from monApp.app import db
from monApp.models import Acheter, TypeBillet
from tests.functional.test_route_paiement import connecter_spectateur


def ajouter_types_billet(testapp):
    with testapp.app_context():
        db.session.add_all([
            TypeBillet(libelle="Pass 1 jour", prix=35.00),
            TypeBillet(libelle="Pass étudiant", prix=25.00),
        ])
        db.session.commit()


def test_confirmer_le_paiement_enregistre_les_billets(client, testapp):
    ajouter_types_billet(testapp)
    connecter_spectateur(client, testapp)
    client.get('/billeterie/selection/1/')

    # deux billets du même type et un autre : trois achats
    response = client.post('/achat/insert/', data={"id_type_billet": ["1", "1", "2"]}, follow_redirects=True)

    assert response.request.path == "/mon-espace/"
    assert "Paiement confirmé".encode() in response.data
    assert "Pass étudiant".encode() in response.data
    with testapp.app_context():
        assert Acheter.query.filter_by(id_spectateur=1).count() == 3
        assert Acheter.query.filter_by(id_spectateur=1, id_type_billet=1).count() == 2
    # la sélection de la billetterie est vidée après l'achat
    response = client.get('/paiement/')
    assert "Aucun billet sélectionné".encode() in response.data


def test_confirmer_sans_billet_ou_avec_un_billet_inconnu(client, testapp):
    ajouter_types_billet(testapp)
    connecter_spectateur(client, testapp)

    response = client.post('/achat/insert/', data={}, follow_redirects=True)
    assert "Aucun billet sélectionné".encode() in response.data

    response = client.post('/achat/insert/', data={"id_type_billet": ["999"]}, follow_redirects=True)
    assert "ne sont plus disponibles".encode() in response.data
    with testapp.app_context():
        assert Acheter.query.count() == 0


def test_confirmer_demande_une_connexion(client, testapp):
    ajouter_types_billet(testapp)
    response = client.post('/achat/insert/', data={"id_type_billet": ["1"]}, follow_redirects=True)
    assert response.request.path == "/connexion/"
    with testapp.app_context():
        assert Acheter.query.count() == 0
