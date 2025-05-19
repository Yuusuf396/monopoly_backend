from django.db import models

class GameResult(models.Model):
    winner = models.CharField(max_length=100)
    strategy = models.CharField(max_length=50)
    turns = models.IntegerField()

    def __str__(self):
        return f"{self.winner} ({self.strategy}) - {self.turns} turns"


class PlayerData(models.Model):
    game = models.ForeignKey(GameResult, on_delete=models.CASCADE, related_name='players')
    name = models.CharField(max_length=100)
    money = models.IntegerField()
    strategy = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - ${self.money} ({self.strategy})"
