from django.db import models
from game.models.game import Game

class CompanyGame(models.Model):
    """Model definition for CompanyGame."""

    def game_settings_default():
        return {"min_bet": 25}
    
    companyId = models.UUIDField()
    game = models.ForeignKey(Game, verbose_name=("Game"), on_delete=models.CASCADE)
    gameSettings = models.JSONField("GameSettings", default=game_settings_default)
    livestream = models.URLField(null=True)
    isDeleted= models.BooleanField(default=False)

    def __str__(self):
        """Unicode representation of CompanyGame."""
        return "<Company Game Id: {self.id}>"

