from django.db import models

class GameDrawType(models.Model):
    """
    Model definition for GameDrawType.
    Default draw close to 5 mins
    """

    companyId = models.CharField(max_length=40)
    gameDrawTypeName = models.CharField(max_length=50)
    openSchedule = models.TimeField()
    endCutOff = models.TimeField()
    drawTime = models.TimeField()
    isDeleted= models.BooleanField(default=False)

    def __str__(self):
        """Unicode representation of GameDrawType."""
        return "<GameDrawType Name: {self.id}>"