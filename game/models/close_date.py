from django.db import models
from game.models.game_draw_type import GameDrawType

class CloseDate(models.Model):
  """Model definition for CloseDate."""

  date = models.DateField()
  isWholeday = models.BooleanField(default=True)
  closedDrawType = models.ForeignKey(GameDrawType, verbose_name=("GameDrawType"), null=True, on_delete=models.CASCADE)
  companyId = models.UUIDField()
  status = models.IntegerField()
  isDeleted= models.BooleanField(default=False)

  def __str__(self):
    """Unicode representation of CloseDate."""
    return "<Closing Date Id: {self.id}>"
