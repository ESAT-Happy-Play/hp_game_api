from django.db import models

class GameDrawType(models.Model):
    """Model definition for GameDrawType."""

    companyId = models.CharField(max_length=40)
    name = models.CharField(max_length=50)
    startTime = models.TimeField()
    cutOff = models.TimeField()

    def __str__(self):
        """Unicode representation of GameDrawType."""
        return "<GameDrawType Name: {self.name}>"
