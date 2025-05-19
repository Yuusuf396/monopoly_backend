from django.urls import path
from .views import GameResultDetailView,GameResultListView,GameResultWinnerDetailView,GameResultByStrategyView,StrategyWinCountView,SimulateGameAPIView

urlpatterns = [
    
    path('simulate/', SimulateGameAPIView.as_view(), name='simulate-game'),

    path('gameresultlist/', GameResultListView.as_view(), name='game-list'),
    path('gameresultlistbystrategy/', StrategyWinCountView.as_view(), name='game-strategy-list'),

    path('gameresultdetail/<int:pk>/', GameResultDetailView.as_view(), name='game-detail'),
    path('gameresults/name/<str:winner>/', GameResultWinnerDetailView.as_view(), name='game-detail-winner'),
    path('gameresults/<str:strategy>/', GameResultByStrategyView.as_view(), name='game-detail-strategy'),
    
    
    
]
 