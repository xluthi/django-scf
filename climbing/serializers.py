from rest_framework import serializers
from climbing.models import Competitor, Result

class CompetitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competitor
        fields = ('id', 'athlete', 'competition', 'category', 'dossard')

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('id', 'competitor', 'boulder', 'result', 'datetime')
