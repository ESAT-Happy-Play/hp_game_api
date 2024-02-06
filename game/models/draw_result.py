from django.db import models
from .game_schedule import GameSchedule

class DrawResult(models.Model):
    """Model definition for DrawResult."""

    gameSchedule = models.ForeignKey(GameSchedule, verbose_name=("GameSchedule"), on_delete=models.CASCADE)
    result = models.CharField(max_length=30)
    amount = models.FloatField()
    noOfWinners = models.IntegerField()
    noOfQuasiWinners = models.IntegerField()
    isDeleted = models.BooleanField(default=False)
    
    def __str__(self):
        """Unicode representation of DrawResult."""
        return "<DrawResult Id: {self.id}>"
