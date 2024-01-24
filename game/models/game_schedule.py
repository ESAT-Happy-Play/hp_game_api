from django.db import models
from game.models.company_game import CompanyGame
from game.models.game_draw_type import GameDrawType
# from game.models.draw_result import DrawResult

class GameSchedule(models.Model):
  """Model definition for GameSchedule."""

  gameDrawType = models.ForeignKey(GameDrawType, verbose_name=("GameDrawType"), on_delete=models.CASCADE)
  companyGame = models.ForeignKey(CompanyGame, verbose_name=("CompanyGame"), on_delete=models.CASCADE)
  drawResult = models.ForeignKey('game.DrawResult', verbose_name=("DrawResult"), on_delete=models.CASCADE)
  date = models.DateField()
  isDeleted= models.BooleanField(default=False)

  def __str__(self):
    """Unicode representation of GameSchedule."""
    return "<GameSchedule Id: {self.id}>"