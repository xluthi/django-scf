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

competitors = compet.competitor_set.all()
boulders = compet.boulder_set.all()
for i in range(10):
    competitor = random.choice(competitors)
    boulder    = random.choice(boulders)
    try:
        r = Result.objects.get(competitor = competitor,
                boulder = boulder)
        print("Result for {} and boulder {} exists: UPDATING".format(r.competitor.athlete, r.boulder.number))
    except:
        r = Result(competitor = competitor,
                boulder = boulder)
        print("Result for {} and boulder {} doesn't exist: CREATING".format(r.competitor.athlete, r.boulder.number))

    #r.result = random.choice(['10', '0', '1', '2'])
    r.result = '2'
    r.save()
