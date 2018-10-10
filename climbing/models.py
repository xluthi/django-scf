# (c) © 2018 Xavier Lüthi xavier@luthi.eu
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# See LICENSE.txt for the full license text.

from django.db import models
from django.core.exceptions import ObjectDoesNotExist

MALE    = 'M'
FEMALE  = 'F'
GENDERS = ( (MALE, "male"), (FEMALE, "female") )

class Gender(models.Model):
    name = models.CharField("Name", max_length=30, unique=True)
    def __str__(self):
        return self.name

class Category(models.Model):
    code = models.CharField("Code", max_length=3, unique=True)
    description = models.CharField("Description", max_length=50)
    gender = models.ForeignKey(Gender, on_delete = models.PROTECT)
    def __str__(self):
        return self.description
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['code']

class Competition(models.Model):
    """
    An Event representing a boulder session.
    """
    code = models.CharField("Event short code", max_length=10, unique=True)
    title = models.CharField("Title", max_length=100)
    date  = models.DateField('Event date')
    description = models.TextField("Event description", blank=True)
    location = models.CharField("Location", blank=True, max_length=100)
    categories  = models.ManyToManyField(Category)
    min_boulder_nbr = models.PositiveIntegerField("Minimum boulder ID", default=1)
    max_boulder_nbr = models.PositiveIntegerField("Maximum boulder ID", default=40)

    def __str__(self):
        return "(" + self.date.isoformat() + ") " + self.title

class Boulder(models.Model):
    number      = models.PositiveIntegerField('ID number', unique=False)
    description = models.CharField('Description', max_length=100, blank=True)
    top_value   = models.PositiveIntegerField('Value for top', default=1000)
    zone_value  = models.PositiveIntegerField('Value for zone', default=0)
    competition = models.ForeignKey(Competition, on_delete = models.CASCADE)
    categories  = models.ManyToManyField(Category)

    @property
    def code(self):
        return "{}-{}".format(self.competition.code, self.number)

    def __str__(self):
        return "({}) {}".format(self.code, self.description)
    class Meta:
        ordering = ["number"]
        unique_together = ('competition', 'number')

    def value(self, category):
        """
        Based on the results, compute the value of the top
        """
        return self.top_value / Result.objects.filter(boulder=self.id, result=2, competitor__category = category).count()

class Club(models.Model):
    name = models.CharField('Name', max_length=100, unique=True)
    city = models.CharField('City', max_length=100)
    gym  = models.CharField('Gym/sport hall', max_length=100)

    def __str__(self):
        return "{} ({})".format(self.name, self.city)

class Athlete(models.Model):
    """
    It represents one individual person, regardless of his/her participation to
    any event.
    When (s)he wants to join a competition, a competitor is created, with a
    specific category, and a specific dossard.
    """
    lastname     = models.CharField('Lastname', max_length=100)
    firstname    = models.CharField('Firstname', max_length=100)
    gender       = models.ForeignKey(Gender, on_delete=models.PROTECT)
    birthdate    = models.DateField('Birthdate')
    club         = models.ForeignKey(Club, on_delete=models.PROTECT, blank=True)
    nationality  = models.CharField('Nationality', max_length=3, default='BEL')

    class Meta:
        ordering = ['lastname', 'firstname']
        unique_together = ('lastname', 'firstname')
    def __str__(self):
        return "{} {}".format(self.firstname, self.lastname)

class Competitor(models.Model):
    """
    A competitor register the participation of an athlete to a specific
    competition.
    """
    athlete     = models.ForeignKey(Athlete,     on_delete = models.PROTECT)
    competition = models.ForeignKey(Competition, on_delete = models.PROTECT)
    category    = models.ForeignKey(Category,    on_delete = models.PROTECT, blank=True)
    dossard     = models.PositiveIntegerField('Dossard', unique=False)

    class Meta:
            unique_together = (('athlete', 'competition'), ('competition', 'dossard'))
            ordering = ['competition', 'dossard']
    def __str__(self):
        return "{}   -   {}   -   ({})  --> {}".format(self.dossard, self.competition, self.category, self.athlete)

class ResultManager(models.Manager):
    def get_result(self, competitor, boulder):
        try:
            return self.get(competitor=competitor, boulder=boulder)
        except self.model.DoesNotExist:
            r = Result()
            r.result = 10
            r.boulder = boulder
            r.competitor = competitor
            return r

class Result(models.Model):
        """
        Each record represents a specific result for an athelete for a specific
        competition for a specific route
        """
        # 10 means "no attempt yet"
        RESULTS = (
            (10, ""),
            (0, "failure"),
            (1, "zone"),
            (2, "top")
        )
        competitor  = models.ForeignKey(Competitor, on_delete = models.CASCADE)
        boulder     = models.ForeignKey(Boulder, on_delete = models.CASCADE)
        result      = models.PositiveSmallIntegerField(choices=RESULTS)
        datetime    = models.DateTimeField('attempt date', auto_now_add=True)
        def __str__(self):
            return "{}, boulder: {}, result: {}".format(self.competitor, self.boulder, self.result)
        objects = ResultManager()
        class Meta:
            unique_together = ('competitor', 'boulder')
