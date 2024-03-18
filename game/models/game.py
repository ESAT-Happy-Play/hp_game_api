from django.db import models

class Game(models.Model):
    """Model definition for Game.
    GameMechanics Structure:{
        "isParent": bool,
        "parentId": int,
        "nCards": int,
        "nSuites": int
    }
    """

    def game_mechanics_default():
        return {"nCards": 3, "nSuites": None}

    name = models.CharField(max_length=100)
    gameMechanics = models.JSONField("GameMechanics", default=game_mechanics_default)
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        """Unicode representation of Game."""
        return f"<Game Id: {self.id}>"
