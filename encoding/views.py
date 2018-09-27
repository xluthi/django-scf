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
    if result != 10:
        result,created  = Result.objects.update_or_create(competitor=competitor,
            boulder=boulder, defaults={'result': result})
    else:
        result = get_object_or_404(Result, competitor=competitor, boulder=boulder)
        result.delete()

    return HttpResponseRedirect(reverse('encoding:competitor', args=(competition.id, competitor.id)))

def list_boulders(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    context =  {'competition': competition}
    return render(request, 'encoding/list_boulders.html', context)


def boulder(request, competition_id, boulder_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    boulder = get_object_or_404(Boulder, pk=boulder_id)
    competitors = competition.competitor_set.all()
    result_set = []
    for competitor in competitors:
        result_set.append(Result.objects.get_result(competitor=competitor, boulder=boulder))
    context = {'competition': competition, 'boulder': boulder, 'competitors': competitors, 'result_set': result_set}
    return render(request, 'encoding/boulder.html', context)


def boulder_encode(request, competition_id, boulder_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    boulder = get_object_or_404(Boulder, pk=boulder_id)
    try:
        competitor = get_object_or_404(Competitor, pk=request.POST['competitor'])
        result           = request.POST['submit']
    except (KeyError):
        return render(request, 'encoding/boulder.html', {
            'competition': competition,
            'boulder': boulder,
            'error_message': 'Résultat invalide.',
        })
    if result != 10:
        result,created  = Result.objects.update_or_create(competitor=competitor,
            boulder=boulder, defaults={'result': result})
    else:
        result = get_object_or_404(Result, competitor=competitor, boulder=boulder)
        result.delete()

    return HttpResponseRedirect(reverse('encoding:boulder', args=(competition.id, boulder.id)))
