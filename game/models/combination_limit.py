from django.db import models
from game.models.company_game import CompanyGame

class CombinationLimit(models.Model):
    """Model definition for CombinationLimit."""

    companyGame = models.ForeignKey(CompanyGame, verbose_name=("CompanyGame"), on_delete=models.CASCADE)
    combination = models.CharField(max_length=20)
    limit = models.FloatField()

    def __str__(self):
        """Unicode representation of CombinationLimit."""
        return "<Combination Limit Id: {self.id}>"
