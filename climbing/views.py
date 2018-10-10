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

from django.http import HttpResponse, HttpResponseRedirect
from .models import Competition, Result, Athlete, Competitor
from django.shortcuts import render, get_object_or_404
from django.urls import reverse


def index(request):
    latest_competition_list = Competition.objects.order_by('-date')[:5]
    context =  {'latest_competition_list': latest_competition_list}
    return render(request, 'climbing/index.html', context)

def athletes_index(request):
    athletes = Athlete.objects.all()
    context = {'athletes': athletes}
    return render(request, 'climbing/athletes_index.html', context)

def athlete(request, athlete_id):
    athlete = get_object_or_404(Athlete, pk=athlete_id)
    return render(request, 'climbing/athlete.html', {'athlete': athlete})



def detail(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    return render(request, 'climbing/detail.html', {'competition': competition})

def results(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    categories = competition.categories.all()
    r = []
    # create a ranking for each category
    for category in categories:
        res_cat = []
        competitors = competition.competitor_set.filter(category=category.id)
        boulders = competition.boulder_set.filter(categories=category.id)
        if len(competitors) == 0:
            # do not compture ranking if no competitor in this category
            continue
        # compute first every boulder value for this Category
        for b in boulders:
            try:
                b.computed_zone = b.zone_value / Result.objects.filter(boulder=b.id, result__in=[1,2], competitor__category = category).count()
            except ZeroDivisionError:
                b.computed_zone = 0
                b.computed_top  = 0
                continue
            try:
                b.computed_top  = b.top_value  / Result.objects.filter(boulder=b.id, result=2, competitor__category = category).count()
            except ZeroDivisionError:
                b.computed_top = 0

        # compute result for each competitor
        for competitor in competitors:
            ra = {}
            ra['competitor'] = competitor
            tops, zones = (0, 0)
            total_score = 0
            boulder_results = []
            for b in boulders:
                score = Result.objects.get_result(competitor=competitor, boulder=b).get_result_display()
                boulder_results.append(score)
                if score == 'top':
                    tops += 1
                    total_score += b.computed_top
                if score == 'zone' or score == 'top':
                    zones += 1
                    total_score += b.computed_zone
            ra['boulders'] = boulder_results
            ra['tops'] = tops
            ra['zones'] = zones
            ra['score'] = total_score
            res_cat.append(ra)
            res_cat.sort(key=lambda x: x['score'], reverse=True)
            if len(res_cat) > 0: res_cat[0]['ranking'] = 1
            for i in range(1,len(res_cat)):
                # define ranking, taking into account ex-aequo
                if res_cat[i]['score'] == res_cat[i-1]['score']:
                    res_cat[i]['ranking'] = res_cat[i-1]['ranking']
                else:
                    res_cat[i]['ranking'] = i+1
        r.append({'category': "{}".format(category), 'boulders': boulders, 'results': res_cat})

    context = {
        'competition' : competition,
        'competitors' : competitors,
        'boulders'    : boulders,
        'results'     : r,
    }
    return render(request, 'climbing/results.html', context)

def athlete_results(request, competition_id, competitor_id):
        competition = get_object_or_404(Competition, pk=competition_id)
        boulders = competition.boulder_set.all()
        competitor = get_object_or_404(Competitor, pk=competitor_id)
        r = []
        for b in boulders:
            r.append(Result.objects.get_result(competitor=competitor, boulder=b).result)
        context = {
            'competition': competition,
            'competitor'   : competitor,
            'results': r,
        }
        return render(request, 'climbing/athlete_results.html', context)


def encode(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    try:
        athlete = competition.athlete_set.get(pk=request.POST['athlete'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'climbing/detail.html', {
            'competition': competition,
            'error_message': "You didn't select an athelete.",
        })
    else:
        res = Result()
        res.competition = competition
        res.boulder_nbr = request.POST['boulder']
        res.result    = request.POST['result']
        res.athlete = athlete

        res.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', args=(competition.id,)))
