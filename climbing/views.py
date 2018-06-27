from django.http import HttpResponse, HttpResponseRedirect
from .models import Competition, Result, Athlete
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
    athletes = competition.athlete_set.all()
    boulders = competition.boulder_set.all()
    r = []
    for a in athletes:
        ra = {}
        ra['athlete'] = a
        # ra.append(str(a))
        tops = 0
        total_score = 0
        boulder_results = []
        for b in boulders:
            score = Result.objects.get_result(athlete=a, boulder=b).result
            boulder_results.append(score)
            if score == 2:
                tops += 1
                total_score += b.value()
        ra['boulders'] = boulder_results
        ra['tops'] = tops
        ra['score'] = total_score
        r.append(ra)
        r.sort(key=lambda x: x['score'], reverse=True)
        if len(r) > 0: r[0]['ranking'] = 1
        for i in range(1,len(r)):
            # define ranking
            if r[i]['score'] == r[i-1]['score']:
                r[i]['ranking'] = r[i-1]['ranking']
            else:
                r[i]['ranking'] = i+1

    context = {
        'competition': competition,
        'athletes'   : athletes,
        'boulders'   : boulders,
        'results'    : r,
    }
    return render(request, 'climbing/results.html', context)

def athlete_results(request, competition_id, athlete_id):
        competition = get_object_or_404(Competition, pk=competition_id)
        boulders = competition.boulder_set.all()
        athlete = get_object_or_404(Athlete, pk=athlete_id)
        r = []
        for b in boulders:
            r.append(Result.objects.get_result(athlete=athlete, boulder=b).result)
        context = {
            'competition': competition,
            'athlete'   : athlete,
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
        return HttpResponseRedirect(reverse('climbing:results', args=(competition.id,)))
