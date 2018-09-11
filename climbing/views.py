from django.http import HttpResponse, HttpResponseRedirect
from .models import Competition, Result, Athlete, Competitor, Club, Boulder, Category
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ResultSerializer, CompetitorSerializer, AthleteSerializer, ClubSerializer
from rest_framework import generics

class ClubList(generics.ListCreateAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
class ClubDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer

class AthleteList(generics.ListCreateAPIView):
    queryset = Athlete.objects.all()
    serializer_class = AthleteSerializer
class AthleteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Athlete.objects.all()
    serializer_class = AthleteSerializer

class CompetitorList(APIView):
    """
    List all competitors, or create a new competitor
    """
    def get(self, request, format=None):
        competitors = Competitor.objects.all()
        serializer = CompetitorSerializer(competitors, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CompetitorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400HTTP_400_BAD_REQUEST)

class CompetitorDetail(APIView):
    """
    Retrieve, update or delete a competitor instance
    """
    def get_object(self, pk):
        try:
            return Competitor.objects.get(pk=pk)
        except Competitor.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        competitor = self.get_object(pk)
        serializer = CompetitorSerializer(competitor)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        competitor = self.get_object(pk)
        serializer = CompetitorSerializer(competitor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        competitor = self.get_object(pk)
        competitor.delete()
        return Response(status=status.HTTP_204HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def result_list(request, format=None):
    """
    List all results, or create a new result.
    """
    if request.method == 'GET':
        results = Result.objects.all()
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def result_detail(request, pk, format=None):
    """
    Retrieve, update or delete a result.
    """
    try:
        result = Result.objects.get(pk=pk)
    except Result.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ResultSerializer(result)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ResultSerializer(result, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        result.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
    boulders = competition.boulder_set.all()
    r = []
    # create a ranking for each category
    for category in categories:
        for gender in ('F', 'M'):
            res_cat = []
            competitors = competition.competitor_set.filter(category=category.id, athlete__gender=gender)
            if len(competitors) == 0:
                # do not compture ranking if no competitor in this category
                continue
            # compute first every boulder value for this Category
            for b in boulders:
                try:
                    b.computed_zone = b.zone_value / Result.objects.filter(boulder=b.id, result__in=[1,2], competitor__category = category, competitor__athlete__gender=gender).count()
                except ZeroDivisionError:
                    b.computed_zone = 0
                    b.computed_top  = 0
                    continue
                try:
                    b.computed_top  = b.top_value  / Result.objects.filter(boulder=b.id, result=2, competitor__category = category, competitor__athlete__gender=gender).count()
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
            r.append({'category': "{} {}".format(category, gender), 'results': res_cat})

    context = {
        'competition': competition,
        'competitors'   : competitors,
        'boulders'   : boulders,
        'results'    : r,
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
        return HttpResponseRedirect(reverse('climbing:results', args=(competition.id,)))
