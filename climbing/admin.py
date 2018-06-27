from django.contrib import admin

# Register your models here.
from .models import Athlete, Competition, Result, Category, Boulder
admin.site.register( (Athlete, Competition, Result, Category, Boulder) )
