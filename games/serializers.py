from .models import GameResult,PlayerData
from rest_framework import serializers

class PlayerDataSerializer(serializers.ModelSerializer):
     class Meta:
        model=PlayerData
        fields=['name','money','strategy',]
     def __str__(self):
        return f"{self.name} (${self.money}) - {self.strategy}"



class GameResultSerializer(serializers.ModelSerializer):
    # players=PlayerDataSerializer(many=True,read_only=True)
    players=PlayerDataSerializer(many=True)
    class Meta:
        model=GameResult
        fields = ['id', 'winner', 'strategy', 'turns', 'players']  # defines what shows in the API
    def __str__(self):
        return f"{self.winner} ({self.strategy}) - {self.turns} turns"

    
    def create(self, validated_data):
        players_data = validated_data.pop('players')  # extract players
        game_result = GameResult.objects.create(**validated_data)  # create game result
        
        # create PlayerData and link them
        for player_data in players_data:
            PlayerData.objects.create(game=game_result, **player_data)
        
        return game_result


class StrategyWinCountSerializer(serializers.Serializer):
    strategy = serializers.CharField()
    wins = serializers.IntegerField()
