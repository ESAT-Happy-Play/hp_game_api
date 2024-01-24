from django.db import models
from game.models.game import Game

class CompanyGame(models.Model):
    """Model definition for CompanyGame."""

    def game_settings_default():
        return {"min_bet": 25}
    
    companyId = models.CharField(max_length=40)
    gameId = models.ForeignKey(Game, verbose_name=("GameId"), on_delete=models.CASCADE)
    gameSettings = models.JSONField("GameSettings", default=game_settings_default)
    isDeleted= models.BooleanField(default=False)

    def __str__(self):
        """Unicode representation of CompanyGame."""
        return "<Company Game Id: {self.id}>"

