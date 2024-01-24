from django.db import models

class CloseDate(models.Model):
    """Model definition for CloseDate."""

    companyId = models.CharField(max_length=40)
    isWholeday = models.BooleanField(default=True)
    drawTypes = models.CharField(max_length=30, blank=False)

    def __str__(self):
        """Unicode representation of CloseDate."""
        return "<Closing Date Id: {self.id}>"
