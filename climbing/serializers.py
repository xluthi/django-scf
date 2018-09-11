from rest_framework import serializers
from climbing.models import Competitor, Result, Athlete

class CompetitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competitor
        fields = ('id', 'athlete', 'competition', 'category', 'dossard')

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('id', 'competitor', 'boulder', 'result', 'datetime')

class AthleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Athlete
        fields = ('id', 'lastname', 'firstname', 'gender', 'birthdate', 'club', 'nationality')
