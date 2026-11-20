# Tests des commandes en ligne [Source : TP 2 — test_loaddb_command ; TP 6]
from monApp.models import *
from monApp.commands import hacher
from monApp.app import db


def test_loaddb_command(runner, testapp):
    file = "monApp/data/data.yml"
    result = runner.invoke(args=["loaddb", file])
    assert result.exit_code == 0
    with testapp.app_context():
        assert Groupe.query.count() == 35
        assert Lieu.query.count() == 13
        assert Journee.query.count() == 6
        assert TypeBillet.query.count() == 4
        assert Spectateur.query.count() == 80
        assert Evenement.query.count() == 41
        unGroupe = Groupe.query.filter_by(nom_groupe="Migos").first()
        assert unGroupe.compositions.count() == 3
        assert db.session.get(Spectateur, 1).mot_de_passe == hacher("demo-emma")


def test_syncdb_command(runner):
    result = runner.invoke(args=["syncdb"])
    assert result.exit_code == 0
