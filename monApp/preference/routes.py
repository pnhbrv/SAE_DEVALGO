from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from . import preference_bp
from .forms import PreferencesForm
from monApp.app import db
from monApp.models import Acheter, Evenement, Groupe, MettreEnFavori, PreferenceStyle, PreInscrire, StyleMusical
from monApp.recommandation import cache, concerts_conseilles, preferences_du_spectateur

# notes possibles : de -5 à +5, sans 0 (pas de préférence = pas de ligne dans la table)
NOTES = [5, 4, 3, 2, 1, -1, -2, -3, -4, -5]


def lire_note(valeur):
    """Renvoie la note choisie, ou None pour « pas d'avis » (ou une valeur qui n'est pas une note)."""
    for note in NOTES:
        if valeur == str(note):
            return note
    return None


def enregistrer_note(id_spectateur, id_style, note):
    unePreference = PreferenceStyle.query.filter_by(id_spectateur=id_spectateur, id_style=id_style).first()
    if note is None:
        if unePreference is not None:
            db.session.delete(unePreference)
    elif unePreference is None:
        db.session.add(PreferenceStyle(id_spectateur=id_spectateur, id_style=id_style, note=note))
    else:
        unePreference.note = note


@preference_bp.route("/mes-styles/", methods=("GET", "POST",))
@login_required
def mesStyles():
    unForm = PreferencesForm()
    id_spectateur = current_user.id_spectateur
    lesStyles = StyleMusical.query.order_by(StyleMusical.id_style).all()
    if unForm.validate_on_submit():
        for unStyle in lesStyles:
            note = lire_note(request.form.get("note_%d" % unStyle.id_style, ""))
            enregistrer_note(id_spectateur, unStyle.id_style, note)
        db.session.commit()
        # les recommandations déjà calculées ne correspondent plus aux nouveaux goûts
        cache.invalider(id_spectateur)
        flash("Vos styles préférés sont enregistrés.", "succes")
        return redirect(url_for("preference.mesStyles"))
    return render_template("mes_styles.html", title="Mes styles préférés", form=unForm, styles=lesStyles,
                           prefs=preferences_du_spectateur(id_spectateur), notes=NOTES)


@preference_bp.route("/mes-concerts-conseilles/")
@login_required
def mesConcertsConseilles():
    id_spectateur = current_user.id_spectateur
    lesEvenements, score_total = concerts_conseilles(id_spectateur)
    a_des_preferences = len(preferences_du_spectateur(id_spectateur)) > 0
    return render_template("mes_concerts_conseilles.html", title="Mes concerts conseillés",
                           evenements=lesEvenements, a_des_preferences=a_des_preferences)


@preference_bp.route("/mon-espace/")
@login_required
def monEspace():
    id_spectateur = current_user.id_spectateur
    lesAchats = Acheter.query.filter_by(id_spectateur=id_spectateur).order_by(Acheter.date_achat).all()
    lesConcerts = Evenement.query.join(PreInscrire, PreInscrire.id_evenement == Evenement.id_evenement)                                  .filter(PreInscrire.id_spectateur == id_spectateur)                                  .order_by(Evenement.date_heure_debut).all()
    lesPreferences = PreferenceStyle.query.filter_by(id_spectateur=id_spectateur)                                           .order_by(PreferenceStyle.note.desc()).all()
    lesFavoris = Groupe.query.join(MettreEnFavori, MettreEnFavori.id_groupe == Groupe.id_groupe)                              .filter(MettreEnFavori.id_spectateur == id_spectateur)                              .order_by(Groupe.nom_groupe).all()
    return render_template("mon_espace.html", title="Mon espace", achats=lesAchats, concerts=lesConcerts,
                           preferences=lesPreferences, favoris=lesFavoris)
