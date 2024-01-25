from django.db import models

class Game(models.Model):
    """Model definition for Game."""

    def game_mechanics_default():
        return {"n_cards": 3, "n_suites": None}

    name = models.CharField(max_length=100)
    gameMechanics = models.JSONField("GameMechanics", default=game_mechanics_default)
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        """Unicode representation of Game."""
        return f"<Game Id: {self.id}>"
