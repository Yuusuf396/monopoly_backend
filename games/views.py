from rest_framework import generics
from rest_framework.views import APIView
from .services import run_and_save_simulation

from rest_framework.response import Response
from rest_framework import status


from .models import GameResult
from .serializers import GameResultSerializer,StrategyWinCountSerializer
from django.db.models import Count
class GameResultListView(generics.ListAPIView):
    queryset=GameResult.objects.all()
    serializer_class=GameResultSerializer
    # permission_classes=
    
    
class GameResultDetailView(generics.RetrieveAPIView):
    queryset = GameResult.objects.all()
    serializer_class = GameResultSerializer
    
    
class GameResultWinnerDetailView(generics.ListAPIView):
    # queryset = GameResult.objects.all()
    serializer_class = GameResultSerializer
    # lookup_field='winner'
    
    def get_queryset(self):
        winner_name = self.kwargs['winner']
        return GameResult.objects.filter(winner=winner_name)
    
    
# class GameResultByStrategyView(generics.ListAPIView):
#     serializer_class=GameResultSerializer
    
#     def get_queryset(self):
#         return GameResult.objects.filter(strategy=self.kwargs['strategy'])

class GameResultByStrategyView(generics.ListAPIView):
    serializer_class = GameResultSerializer

    def get_queryset(self):
        queryset = GameResult.objects.all()
        strategy = self.kwargs['strategy']  # ✅ path param (matches /gameresults/<strategy>/)

        if strategy:
            queryset = queryset.filter(strategy=strategy)
        return queryset

class StrategyWinCountView(generics.ListAPIView):
    
    serializer_class = StrategyWinCountSerializer
    pagination_class = None 

    def get_queryset(self):
        # This returns a list of dicts like [{'strategy': 'AGGRESSIVE', 'wins': 120}, ...]
        return (
            GameResult.objects
            .values('strategy')
            .annotate(wins=Count('id'))
            .order_by('-wins')
        )
        
class SimulateGameAPIView(APIView):
    def post(self, request):
        try:
            run_and_save_simulation()   
            return Response({"message": "New simulation created."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)