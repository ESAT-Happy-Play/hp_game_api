from django.db import models
from .game_schedule import GameSchedule
from .company_game import CompanyGame

class PrizePool(models.Model):
    """Model definition for PrizePool."""

    companyId = models.UUIDField()
    gameSchedule = models.OneToOneField(GameSchedule, verbose_name=("GameSchedule"), on_delete=models.CASCADE)
    companyGame = models.ForeignKey(CompanyGame, verbose_name=("CompanyGame"), on_delete=models.CASCADE)
    winningPrize = models.FloatField()
    totalBets = models.IntegerField()
    totalBetsAmount = models.IntegerField()
    cardPrice = models.IntegerField()
    specialDraw = models.BooleanField(default=False)
    hasWinner = models.BooleanField(default=False)
    hasDrawn = models.BooleanField(default=False)
    isDeleted = models.BooleanField(default=False)
    
    def __str__(self):
        """Unicode representation of PrizePool."""
        return "<PrizePool Id: {self.id}>"
