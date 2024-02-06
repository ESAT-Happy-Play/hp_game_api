from django.db import models
from game.models.draw_result import DrawResult
from .bet_item import BetItem

class DrawResultWinner(models.Model):
    """Model definition for DrawResultWinner."""

    drawResult = models.ForeignKey(DrawResult, related_name='drawResultWinner', on_delete=models.CASCADE)
    accountInfoId = models.CharField(max_length=40)
    amount = models.FloatField()
    betInfo = models.ForeignKey(BetItem, related_name='drawResultWinner', on_delete=models.CASCADE)
    isQuasi = models.BooleanField(default=False)
    isDeleted = models.BooleanField(default=False)
    
    def __str__(self):
        """Unicode representation of DrawResultsWinner."""
        return "<DrawResultsWinner Id: {self.id}>"
