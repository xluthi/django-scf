import sys
sys.path.append("..")
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stone.settings")
django.setup()

from climbing.models import Competition, Category, Athlete, Competitor, Club, Boulder

clubs = [
    {'name': 'New Rock', 'city': 'Auderghem, Bruxelles', 'gym': 'New Rock'},
    {'name': 'Evolution Verticale', 'city': 'Woluwé-Saint-Pierre, Bruxelles', 'gym': 'Poseidon'},
    {'name': 'Brussels Monkey Climbing', 'city': 'Molenbeek, Bruxelles', 'gym': 'Stadium'},
    {'name': 'Entre Ciel et Terre', 'city': 'Louvain-la-Neuve', 'gym': 'Blocry'},
    {'name': 'Rêvolution Climbing Team', 'city': 'none', 'gym': 'none'},
    {'name': 'Altitude CCM', 'city': 'Braine-L\'Alleud', 'gym': 'Centre sportif Cardinal Mercier'},
    {'name': 'autre club', 'city': 'none', 'gym': 'none'},
    {'name': 'pas de club', 'city': 'none', 'gym': 'none'},
]

for club in clubs:
    c = Club(name=club['name'], city=club['city'], gym=club['gym'])
    c.save()
