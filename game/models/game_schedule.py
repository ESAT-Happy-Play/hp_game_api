from django.db import models
from game.models.company_game import CompanyGame
from game.models.game_draw_type import GameDrawType
# from game.models.draw_result import DrawResult

class GameSchedule(models.Model):
  """Model definition for GameSchedule."""

  gameDrawTypeId = models.ForeignKey(GameDrawType, verbose_name=("GameDrawType"), on_delete=models.CASCADE)
  companyGameId = models.ForeignKey(CompanyGame, verbose_name=("CompanyGameId"), on_delete=models.CASCADE)
  drawResultId = models.ForeignKey('game.DrawResult', verbose_name=("DrawResultId"), on_delete=models.CASCADE)
  date = models.DateField()
  isDeleted= models.BooleanField(default=False)

  def __str__(self):
    """Unicode representation of GameSchedule."""
    return "<GameSchedule Id: {self.id}>"