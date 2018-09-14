from rest_framework import serializers
from climbing.models import Competitor, Result, Athlete, Club, Category, Competition, Boulder
from climbing.views import *

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('id', 'competitor', 'boulder', 'result', 'datetime')

class CompetitorSerializer(serializers.ModelSerializer):
    athlete = serializers.HyperlinkedRelatedField(read_only=True, view_name='athlete-detail')
    result_set = ResultSerializer(many=True)
    class Meta:
        model = Competitor
        fields = ('id', 'athlete', 'competition', 'category', 'dossard', 'result_set')

class AthleteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Athlete
        fields = ('url', 'lastname', 'firstname', 'gender', 'birthdate', 'club', 'nationality')

class ClubSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Club
        fields = ('url', 'name', 'city', 'gym')
