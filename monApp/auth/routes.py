# Vues d'authentification [Source : TP 6 — login, logout, next ; TP 5 — vue GET + traitement POST]
from flask import redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from . import auth_bp
from monApp.app import db
from monApp.auth.forms import InscriptionForm, LoginForm
from monApp.commands import hacher
from monApp.models import Spectateur


@auth_bp.route("/compte/")
def compte():
    # page d'accueil du compte : « Se connecter » / « Créer votre compte » [Source : Exemple.png — /index]
    return render_template("compte.html", title="Mon compte")


@auth_bp.route("/connexion/", methods=("GET", "POST",))
def login():
    unForm = LoginForm()
    unUser = None
    if not unForm.is_submitted():
        unForm.next.data = request.args.get('next')
    elif unForm.validate_on_submit():
        unUser = unForm.get_authenticated_user()
        if unUser:
            login_user(unUser)
            next = unForm.next.data or url_for("menu.index")
            return redirect(next)
    return render_template("login.html", title="Connexion", form=unForm)


@auth_bp.route("/inscription/", methods=("GET", "POST",))
def inscription():
    unForm = InscriptionForm()
    if unForm.validate_on_submit():
        if Spectateur.query.filter_by(email=unForm.email.data).first() is not None:
            # ⚠️ message à valider : l'email est UNIQUE dans Creation.sql
            unForm.email.errors.append("Ce mail est déjà utilisé.")
        else:
            unSpectateur = Spectateur(nom=unForm.nom.data, prenom=unForm.prenom.data, email=unForm.email.data,
                                      mot_de_passe=hacher(unForm.mot_de_passe.data))
            db.session.add(unSpectateur)
            db.session.commit()
            return redirect(url_for("auth.login"))
    return render_template("inscription.html", title="Inscription", form=unForm)


@auth_bp.route("/deconnexion/")
def logout():
    logout_user()
    return redirect(url_for('menu.index'))
