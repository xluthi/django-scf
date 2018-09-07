import sys
sys.path.append("..")
import os, django, random, datetime
from django.db.models import Max
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stone.settings")
django.setup()

from climbing.models import Competition, Category, Athlete, Competitor, Club, Boulder
compet = Competition.objects.get(code='SCF1')

prenoms = [
    'Jitse',
    'Casimir',
    'Corentin',
    'Lars',
    'Alexandre',
    'Célian',
    'Antonin',
    'Joppe',
    'Stef',
    'Victor',
    'Thor',
    'Korneel',
    'Aloîs',
    'Noah',
    'Manu',
    'Aaron',
    'Jannes',
    'Willem',
    'Aaron',
    'Brent',
    'Igor',
    'Sander',
    'Tristan',
    'Guillaume',
    'Julien',
    'Tibbe',
    'Rune',
    'Pierre',
    'Lionel',
    'Kasper',
    'Rossen',
    'Wolf',
    'Gaston',
    'Arthur',
    'Tristan'
]

noms = [
    'Remes',
    'de Mits',
    'Laporte',
    'Vanhove',
    'Noël',
    'Lescaut',
    'Lüthi',
    'van der Aa',
    'Reweghs',
    'Beaujean',
    'Gijsbers',
    'Vrij',
    'Donéa',
    'Harris',
    'Rogiers',
    'de Bruyn',
    'van de Ven',
    'Vermeeren',
    'Vrancken',
    'Vanhove',
    'Tacq',
    'Dierickx',
    'Noels',
    'Cabergs',
    'Ameye',
    'Apers',
    'Gillis',
    'Broekaert',
    'Windey',
    'van der Bracht',
    'Chapanov',
    'Maes',
    'Rollier',
    'Moerman',
    'Vandamme'
]

clubs = Club.objects.all()
categories = Category.objects.all()

dossard_max = Competitor.objects.filter(competition=compet).aggregate(Max('dossard'))['dossard__max']

for i in range(0, 10):
    a = Athlete(lastname=noms[random.randrange(len(noms))] + " " + str(i),
                firstname=prenoms[random.randrange(len(prenoms))],
                gender=random.choice(['M', 'F']),
                birthdate=datetime.date.today(),
                club=random.choice(clubs))
    a.save()
    competitor = Competitor(athlete=a, competition=compet, dossard=dossard_max+i+1, category=random.choice(categories))
    competitor.save()
