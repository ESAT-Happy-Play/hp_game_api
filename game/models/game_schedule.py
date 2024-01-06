from django.db import models
from game.models.company_game import CompanyGame
from game.models.game_draw_type import GameDrawType

class GameSchedule(models.Model):
    """Model definition for CompanyGame."""

    date = models.DateField()
    gameDrawTypeId = models.ForeignKey(GameDrawType, verbose_name=("GameDrawType"), on_delete=models.CASCADE)
    companyGameId = models.ForeignKey(CompanyGame, verbose_name=("CompanyGameId"), on_delete=models.CASCADE)
    drawResultId = models.IntegerField()

    def __str__(self):
        """Unicode representation of CompanyGame."""
        return "<GameSchedule Id: {self.id}>"