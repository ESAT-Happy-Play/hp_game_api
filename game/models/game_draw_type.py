from django.db import models
from game.models.company import Company

class GameDrawType(models.Model):
    """Model definition for GameDrawType."""

    companyId = models.ForeignKey(Company, verbose_name=("CompanyId"), on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    startTime = models.TimeField()
    cutOff = models.TimeField()

    def __str__(self):
        """Unicode representation of GameDrawType."""
        return "<GameDrawType Name: {self.name}>"
