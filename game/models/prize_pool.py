from django.db import models
from game.models.game_schedule import GameSchedule
from game.models.company_game import CompanyGame

class PrizePool(models.Model):
    """Model definition for PrizePool."""

    gameSchedule = models.ForeignKey(GameSchedule, verbose_name=("GameSchedule"), on_delete=models.CASCADE)
    companyGame = models.ForeignKey(CompanyGame, verbose_name=("CompanyGame"), on_delete=models.CASCADE)
    winningPrize = models.FloatField()
    totalBets = models.IntegerField()
    totalBetsAmount = models.IntegerField()
    cardPrice = models.IntegerField(nullable=True)
    specialDraw = models.BooleanField(default=False)
    isDeleted = models.BooleanField(default=False)
    
    def __str__(self):
        """Unicode representation of PrizePool."""
        return "<PrizePool Id: {self.id}>"
