import sys
sys.path.append("..")
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stone.settings")
django.setup()

from climbing.models import Competition, Category, Athlete, Competitor, Club, Boulder, Result
import random

try:
    compet = Competition.objects.get(code='SCF1')
    print('La compétition SCF1 existe déjà: bien :-)')
except:
    print("La compétition SCF1 n'existe pas, veuillez d'abord la créer.")
    exit()


boulders = compet.boulder_set.all()
for b in boulders:
    b.zone_value = 500
    b.top_value = 1000
    b.save()
