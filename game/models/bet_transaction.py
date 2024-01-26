from django.db import models

class BetTransaction(models.Model):
  """Model definition for CloseDate."""

  transactionNumber = models.CharField(max_length=16)
  orderId = models.BigIntegerField()
  totalAmount = models.FloatField()
  dateOfTransaction = models.DateField()
  accountId = models.BigIntegerField()
  numberOfBets = models.IntegerField()
  betType = models.IntegerField()
  isDeleted= models.BooleanField(default=False)

  def __str__(self):
    """Unicode representation of BetTransaction."""
    return "<Bet Transaction Id: {self.id}>"
