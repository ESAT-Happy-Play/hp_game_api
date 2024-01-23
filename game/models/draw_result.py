from django.db import models
from game.models.game_schedule import GameSchedule

class DrawResult(models.Model):
    """Model definition for DrawResult."""

    gameScheduleId = models.ForeignKey(GameSchedule, verbose_name=("GameScheduleId"), on_delete=models.CASCADE)
    result = models.CharField(max_length=30)
    amount = models.DecimalField()
    noOfWinners = models.IntegerField()
    isDeleted = models.BooleanField(default=False)
    
    def __str__(self):
        """Unicode representation of DrawResult."""
        return "<DrawResult Id: {self.id}>"
