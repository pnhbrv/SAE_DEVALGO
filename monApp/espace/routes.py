from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from . import espace_bp
from monApp.app import db
from monApp.models import Acheter, PreferenceStyle, StyleMusical


@espace_bp.route('/espace/')
@login_required
def getEspace():
    lesConcerts = sorted([uneInscription.evenement for uneInscription in current_user.pre_inscriptions.all()],
                         key=lambda e: e.date_heure_debut)
    lesPreferences = current_user.preferences.order_by(PreferenceStyle.note.desc()).all()
    return render_template("espace.html", title="Mon espace",
                           achats=current_user.achats.order_by(Acheter.date_achat).all(),
                           concerts=lesConcerts,
                           aimes=[p for p in lesPreferences if p.note > 0],
                           pas_aimes=[p for p in lesPreferences if p.note < 0],
                           favoris=[unFavori.groupe for unFavori in current_user.favoris.all()])


@espace_bp.route('/espace/styles/', methods=("GET", "POST",))
@login_required
def modifierStyles():
    unForm = FlaskForm()
    lesStyles = StyleMusical.query.order_by(StyleMusical.libelle_style).all()
    if unForm.validate_on_submit():
        for unStyle in lesStyles:
            note = request.form.get('note_%s' % unStyle.id_style, 0, type=int)
            note = max(-5, min(5, note))
            unePref = db.session.get(PreferenceStyle, (current_user.id_spectateur, unStyle.id_style))
            if note == 0:
                if unePref is not None:
                    db.session.delete(unePref)
            elif unePref is None:
                db.session.add(PreferenceStyle(current_user.id_spectateur, unStyle.id_style, note))
            else:
                unePref.note = note
        db.session.commit()
        flash("Vos styles préférés ont été mis à jour.", "succes")
        return redirect(url_for('espace.getEspace'))
    lesNotes = {unePref.id_style: unePref.note for unePref in current_user.preferences.all()}
    return render_template("modifier_styles.html", title="Mes styles préférés", form=unForm,
                           styles=lesStyles, notes=lesNotes)
