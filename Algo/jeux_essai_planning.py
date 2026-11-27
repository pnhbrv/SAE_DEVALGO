"""Jeux d'essai pour le planning, le cache et la recommandation complète (1.7).

Contient :
- une programmation réaliste sur une journée complète de festival (14h à 4h du matin),
  avec plusieurs scènes, des concerts multi-genres et des chevauchements ;
- plusieurs profils de festivaliers (préférences ciblées et cas limites) ;
- des cas limites dédiés au planning (trajets, minuit, conflits, égalités).
"""
from datetime import datetime
from jeu_essai import ID
from modeles import Concert


# Programmation réaliste d'une journée (10 juillet 14h -> 11 juillet 04h) sur 4 scènes
PROGRAMMATION_JOURNEE = [
    Concert(1, datetime(2026, 7, 10, 14, 0), datetime(2026, 7, 10, 15, 15),
            genres=[ID["Folk rock"]], lieu="Scène Acoustique"),
    Concert(2, datetime(2026, 7, 10, 14, 30), datetime(2026, 7, 10, 15, 45),
            genres=[ID["Pop"], ID["Synth-pop"]], lieu="Grande Scène"),
    Concert(3, datetime(2026, 7, 10, 15, 30), datetime(2026, 7, 10, 16, 45),
            genres=[ID["Punk rock"], ID["Pop punk"]], lieu="Scène Bleue"),
    Concert(4, datetime(2026, 7, 10, 16, 0), datetime(2026, 7, 10, 17, 15),
            genres=[ID["House"]], lieu="La Bulle Électro"),
    Concert(5, datetime(2026, 7, 10, 17, 0), datetime(2026, 7, 10, 18, 15),
            genres=[ID["Rock"], ID["Garage rock"]], lieu="Grande Scène"),
    Concert(6, datetime(2026, 7, 10, 18, 0), datetime(2026, 7, 10, 19, 15),
            genres=[ID["Hip-hop"], ID["Trap"]], lieu="Scène Bleue"),
    Concert(7, datetime(2026, 7, 10, 18, 30), datetime(2026, 7, 10, 20, 0),
            genres=[ID["Deep house"]], lieu="La Bulle Électro"),
    Concert(8, datetime(2026, 7, 10, 19, 30), datetime(2026, 7, 10, 21, 0),
            genres=[ID["Rock"], ID["Folk punk"]], lieu="Grande Scène"),
    Concert(9, datetime(2026, 7, 10, 20, 15), datetime(2026, 7, 10, 21, 45),
            genres=[ID["New wave"], ID["Synth-pop"]], lieu="Scène Acoustique"),
    Concert(10, datetime(2026, 7, 10, 21, 15), datetime(2026, 7, 10, 22, 45),
            genres=[ID["Drill"], ID["Trap"]], lieu="Scène Bleue"),
    Concert(11, datetime(2026, 7, 10, 21, 30), datetime(2026, 7, 10, 23, 0),
            genres=[ID["Rock"], ID["Punk rock"]], lieu="Grande Scène"),
    # Passage de minuit
    Concert(12, datetime(2026, 7, 10, 23, 15), datetime(2026, 7, 11, 0, 45),
            genres=[ID["Techno"], ID["Minimal techno"]], lieu="La Bulle Électro"),
    Concert(13, datetime(2026, 7, 10, 23, 30), datetime(2026, 7, 11, 1, 0),
            genres=[ID["Hip-hop"], ID["Cloud rap"]], lieu="Grande Scène"),
    Concert(14, datetime(2026, 7, 11, 1, 15), datetime(2026, 7, 11, 2, 30),
            genres=[ID["House"], ID["Deep house"]], lieu="La Bulle Électro"),
    Concert(15, datetime(2026, 7, 11, 1, 30), datetime(2026, 7, 11, 3, 0),
            genres=[ID["Garage punk"]], lieu="Scène Bleue"),
    Concert(16, datetime(2026, 7, 11, 2, 45), datetime(2026, 7, 11, 4, 0),
            genres=[ID["Électro"], ID["House"]], lieu="La Bulle Électro"),
]


# Profils de festivaliers représentatifs
PROFIL_ROCK = {ID["Rock"]: 5, ID["Garage rock"]: -3, ID["Hip-hop"]: 2}
PROFIL_ELECTRO = {ID["Électro"]: 4, ID["Techno"]: -4}
PROFIL_RAP = {ID["Hip-hop"]: 5, ID["Pop"]: -2}

# Profils limites
PROFIL_SANS_PREFERENCE = {}
PROFIL_FAN_DE_TOUT = {
    ID["Rock"]: 5,
    ID["Hip-hop"]: 5,
    ID["Électro"]: 5,
    ID["Pop"]: 5,
}
PROFIL_REFUSE_TOUT = {
    ID["Rock"]: -5,
    ID["Hip-hop"]: -5,
    ID["Électro"]: -5,
    ID["Pop"]: -5,
}
