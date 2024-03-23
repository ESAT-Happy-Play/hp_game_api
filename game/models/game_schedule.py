from django.db import models
from .company_game import CompanyGame
from .game_draw_type import GameDrawType

class GameSchedule(models.Model):
  """Model definition for GameSchedule."""

  companyId = models.UUIDField()
  gameDrawType = models.ForeignKey(GameDrawType, related_name=("gameSchedule"), on_delete=models.CASCADE)
  companyGame = models.ForeignKey(CompanyGame, related_name=("gameSchedule"), on_delete=models.CASCADE)
  date = models.DateField()
  drawTime = models.TimeField()
  openSchedule = models.TimeField()
  endCutOff = models.TimeField()
  status = models.IntegerField() # 0-not yet drawn, 1-drawn
  isDeleted= models.BooleanField(default=False)

  def __str__(self):
    """Unicode representation of GameSchedule."""
    return "<GameSchedule Id: {self.id}>"