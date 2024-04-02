from django.db import models
from game.models.company_game import CompanyGame

class WinStreak(models.Model):
    """Model definition for WinStreak."""

    accountId = models.BigIntegerField()
    streak = models.IntegerField()
    companyGame = models.ForeignKey(CompanyGame, verbose_name=("CompanyGame"), on_delete=models.CASCADE)
    
    def __str__(self):
        """Unicode representation of WinStreak."""
        return "<WinStreak Id: {self.id}>"
