from django.db import models
from django.db.models.expressions import RawSQL
from django.db.models.fields.generated import GeneratedField

class BetTransaction(models.Model):
  """Model definition for CloseDate."""

  totalAmount = models.FloatField()
  dateOfTransaction = models.DateField()
  accountId = models.BigIntegerField()
  numberOfBets = models.IntegerField()
  betType = models.IntegerField()
  isDeleted= models.BooleanField(default=False)

  transactionNumber = GeneratedField(
    expression=RawSQL("('HPTRN' || LPAD(id::text, 11, '0'))",()),
    output_field=models.TextField(),
    db_persist=True)


  def __str__(self):
    """Unicode representation of BetTransaction."""
    return f"<Bet Transaction Id: {self.id}>"
  