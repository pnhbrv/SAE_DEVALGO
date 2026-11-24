# Formulaires d'authentification [Source : TP 6 — LoginForm, get_authenticated_user ; TP 5 — DataRequired]
from flask_wtf import FlaskForm
from wtforms import HiddenField, PasswordField, StringField
from wtforms.validators import DataRequired
from monApp.models import Spectateur
from monApp.commands import hacher


class LoginForm(FlaskForm):
    Login = StringField('Votre mail', validators=[DataRequired()])
    Password = PasswordField('Votre mot de passe', validators=[DataRequired()])
    next = HiddenField()

    def get_authenticated_user(self):
        # le spectateur se connecte avec son email
        unUser = Spectateur.query.filter_by(email=self.Login.data).first()
        if unUser is None:
            return None
        return unUser if hacher(self.Password.data) == unUser.mot_de_passe else None


class InscriptionForm(FlaskForm):
    # champs de la maquette /inscription = colonnes de SPECTATEUR
    nom = StringField('Votre nom', validators=[DataRequired()])
    prenom = StringField('Votre prénom', validators=[DataRequired()])
    email = StringField('Votre mail', validators=[DataRequired()])
    mot_de_passe = PasswordField('Votre mot de passe', validators=[DataRequired()])
