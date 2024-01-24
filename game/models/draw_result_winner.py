from django.db import models
from game.models.draw_result import DrawResult

class DrawResultWinner(models.Model):
    """Model definition for DrawResultWinner."""

    drawResultId = models.ForeignKey(DrawResult, verbose_name=("DrawResultId"), on_delete=models.CASCADE)
    accountInfoId = models.CharField(max_length=40)
    amount = models.FloatField()
    betInfoId = models.CharField(max_length=40)
    isDeleted = models.BooleanField(default=False)
    
    def __str__(self):
        """Unicode representation of DrawResultsWinner."""
        return "<DrawResultsWinner Id: {self.id}>"
