from climbing.models import Competition, Result, Athlete, Competitor, Boulder
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

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

def encode(request, competition_id, competitor_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    competitor  = get_object_or_404(Competitor,  pk=competitor_id)
    try:
        boulder = get_object_or_404(Boulder, pk=request.POST['boulder'])
        result           = request.POST['submit']
    except (KeyError):
        return render(request, 'encoding/competitor.html', {
            'competition': competition,
            'competitor': competitor,
            'error_message': 'Résultat invalide.',
        })

    result,created  = Result.objects.update_or_create(competitor=competitor,
        boulder=boulder, defaults={'result': result})

    return HttpResponseRedirect(reverse('encoding:competitor', args=(competition.id, competitor.id)))
