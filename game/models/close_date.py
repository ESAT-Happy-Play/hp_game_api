from django.db import models
from game.models.company import Company

class CloseDate(models.Model):
    """Model definition for CloseDate."""

    companyId = models.ForeignKey(Company, on_delete=models.CASCADE)
    isWholeday = models.BooleanField(default=True)
    drawTypes = models.CharField(max_length=30, blank=False)

    def __str__(self):
        """Unicode representation of CloseDate."""
        return "<Closing Date Id: {self.id}>"
