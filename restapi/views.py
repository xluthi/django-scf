from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from climbing.models import Competition, Result, Athlete, Competitor, Club, Boulder, Category
from .serializers import ResultSerializer, CompetitorSerializer, AthleteSerializer, ClubSerializer

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
        serializer = CompetitorSerializer(competitor, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        competitor = self.get_object(pk)
        serializer = CompetitorSerializer(competitor, data=request.data, context={'request': request})
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
        serializer = ResultSerializer(results, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ResultSerializer(data=request.data, context={'request': request})
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
