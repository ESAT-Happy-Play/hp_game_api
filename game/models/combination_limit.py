from django.db import models
from .company_game import CompanyGame
from .game import Game

class CombinationLimit(models.Model):
    """Model definition for CombinationLimit."""

    companyId = models.UUIDField()
    gameId = models.ForeignKey(Game, verbose_name=("Game"), on_delete=models.CASCADE)
    companyGame = models.ForeignKey(CompanyGame, verbose_name=("CompanyGame"), on_delete=models.CASCADE)
    combination = models.CharField(max_length=20)
    limit = models.FloatField()

    def __str__(self):
        """Unicode representation of CombinationLimit."""
        return "<Combination Limit Id: {self.id}>"
