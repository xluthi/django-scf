from django.shortcuts import render
from climbing.models import Competition, Result, Athlete, Competitor
from django.shortcuts import render, get_object_or_404

def competition(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    context =  {'competition': competition}
    return render(request, 'encoding/competition.html', context)

def competitor(request, competition_id, competitor_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    competitor  = get_object_or_404(Competitor,  pk=competitor_id)
    boulders = competition.boulder_set.all()
    result_set = []
    for boulder in boulders:
        result_set.append(Result.objects.get_result(competitor=competitor, boulder=boulder))
    context = {'competition': competition, 'boulders': boulders, 'competitor': competitor, 'result_set': result_set}
    return render(request, 'encoding/competitor.html', context)
