from django.db import models
from django.contrib.postgres.fields import ArrayField

class CloseDate(models.Model):
  """Model definition for CloseDate."""

  isWholeday = models.BooleanField(default=True)
  closedDrawTypes = ArrayField(models.IntegerField(), default=list, blank=True)
  companyId = models.CharField(max_length=40)
  isDeleted= models.BooleanField(default=False)

  def __str__(self):
    """Unicode representation of CloseDate."""
    return "<Closing Date Id: {self.id}>"
