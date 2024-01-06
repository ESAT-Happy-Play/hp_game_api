from django.db import models

class Company(models.Model):
    """Model definition for Company."""

    companyObjectId = models.IntegerField()
    name = models.CharField(max_length=75)

    def __str__(self):
        """Unicode representation of Company."""
        return "<Company Id: {self.id}>"
