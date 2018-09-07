import sys
sys.path.append("..")
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stone.settings")
django.setup()

from climbing.models import Competition, Category, Athlete, Competitor, Club, Boulder
import random

scf = Club.objects.get(name='Stone Climbing Factory')
try:
    compet = Competition.objects.get(code='SCF1')
    print('La compétition SCF1 existe déjà: bien :-)')
except:
    print("La compétition SCF1 n'existe pas, veuillez d'abord la créer.")
    exit()



noms = [
    'rock',
    'rocher',
    'dévers',
    'escalier',
    'pic',
    'effort',
    'guépard',
    'serpent',
    'problème',
    ]
attributs = [
    'agile',
    'intrépide',
    'glissant',
    'rapide',
    'impossible',
    'aigü',
    'facile',
    'vertical',
    'de malade',
    'démentiel',
]

for i in range(0, 40):
    name = "{} {}".format(noms[random.randrange(len(noms))], attributs[random.randrange(len(attributs))] )
    b = Boulder(number = i+1, description = name, competition = compet)
    b.save()
