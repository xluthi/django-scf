from django.db import models
from django.core.exceptions import ObjectDoesNotExist

MALE    = 'M'
FEMALE  = 'F'
GENDERS = ( (MALE, "male"), (FEMALE, "female") )

class Category(models.Model):
    code = models.CharField("Code", max_length=3)
    description = models.CharField("Description", max_length=50)
    def __str__(self):
        return "{} - {}".format(self.code, self.description)
    class Meta:
        verbose_name_plural = "Categories"

class Competition(models.Model):
    """
    An Event representing a boulder session.
    """
    title = models.CharField("Title", max_length=100)
    date  = models.DateField('Event date')
    description = models.TextField("Event description", blank=True)
    location = models.CharField("Location", blank=True, max_length=100)
    code = models.CharField("Event short code", max_length=10)
    categories  = models.ManyToManyField(Category)
    min_boulder_nbr = models.PositiveIntegerField("Minimum boulder ID", default=1)
    max_boulder_nbr = models.PositiveIntegerField("Maximum boulder ID", default=40)

    def __str__(self):
        return "(" + self.date.isoformat() + ") " + self.title

class Boulder(models.Model):
    number      = models.PositiveIntegerField('ID number', unique=True)
    description = models.CharField('Description', max_length=100, blank=True)
    top_value   = models.PositiveIntegerField('Value for top', default=1000)
    zone_value  = models.PositiveIntegerField('Value for zone', default=0)
    competition = models.ForeignKey(Competition, on_delete = models.CASCADE)

    def code(self):
        return "{}-{}".format(self.competition.code, self.number)

    def __str__(self):
        return "({}) {}".format(self.code(), self.description)
    class Meta:
        ordering = ["number"]

    def value(self):
        """
        Based on the results, compute the value of the top
        """
        return self.top_value / Result.objects.filter(boulder=self.id, result=2).count()

class Athlete(models.Model):

    # CATEGORIES = (
        # ("D", "D"),
        # ("C", "C"),
        # ("B", "B"),
        # ("A", "A"),
        # ("J", "Junior"),
        # ("S", "Senior"),
        # ("V", "Veteran"),
        # ("P", "para")
    # )

    lastname     = models.CharField('Lastname', max_length=100)
    firstname    = models.CharField('Firstname', max_length=100)
    gender       = models.CharField('Gender', max_length=1, choices=GENDERS, default=MALE)
    birthdate    = models.DateField('Birthdate')
    club         = models.CharField('Club', max_length=100)
    nationality  = models.CharField('Nationality', max_length=3, default='BEL')
    # category     = models.CharField('Category', max_length=1, choices=CATEGORIES, default='C')
    # category     = models.ForeignKey(Category, on_delete = models.CASCADE)
    competitions = models.ManyToManyField(Competition, blank=True)

    class Meta:
        ordering = ['lastname', 'firstname']
    def __str__(self):
        return "{} {}".format(self.firstname, self.lastname)

# class Subcompetition(models.Model):
    # """
    # A part of a competition, specific to a category.
    # For exemple: Boulder Cup 2018 round 1 cat. C

    # This will generate a specific classement for the competition
    # """
    # competition   = models.ForeignKey(Competition, on_delete = models.CASCADE)
    # category      = models.ForeignKey(Category, on_delete = models.PROTECT)
    # gender        = models.CharField('Gender', max_length=1, choices=GENDERS, default=MALE)
    # description   = models.CharField(max_length=100, blank=True)
    # min_route_nbr = models.PositiveIntegerField("Minimum route ID", default=1)
    # max_route_nbr = models.PositiveIntegerField("Maximum route ID", default=40)
    # top_value   = models.PositiveIntegerField('Value for top', default=1000)
    # zone_value  = models.PositiveIntegerField('Value for zone', default=0)
    # def __str__(self):
        # return "{} {} - {} - {}".format(self.category.code, self.gender, self.competition, self.description)

class ResultManager(models.Manager):
    def get_result(self, athlete, boulder):
        try:
            return self.get(athlete=athlete, boulder=boulder)
        except self.model.DoesNotExist:
            print("exception catched")
            r = Result()
            r.result = 0
            return r

class Result(models.Model):
        """
        Each record represents a specific result for an athelete for a specific
        competition for a specific route
        """
        RESULTS = (
            (0, "failure"),
            (1, "zone"),
            (2, "top")
        )
        # competition = models.ForeignKey(Competition, on_delete = models.PROTECT)
        athlete     = models.ForeignKey(Athlete,        on_delete = models.PROTECT)
        boulder     = models.ForeignKey(Boulder, on_delete = models.PROTECT)
        result      = models.PositiveSmallIntegerField(choices=RESULTS)
        def __str__(self):
            return "{}, boulder: {}, result: {}".format(self.athlete, self.boulder, self.result)
        objects = ResultManager()
