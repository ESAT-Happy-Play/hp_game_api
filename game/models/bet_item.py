from django.db import models
from game.models.company_game import CompanyGame
from game.models.game_schedule import GameSchedule
from game.models.bet_transaction import BetTransaction

class BetItem(models.Model):
    """Model definition for BetItem."""

    value = models.CharField(max_length=20)
    orderItemId = models.BigIntegerField()
    amount = models.IntegerField()
    betTransaction = models.ForeignKey(BetTransaction, related_name=("betItem"), on_delete=models.CASCADE)
    companyGame = models.ForeignKey(CompanyGame, related_name=("betItem"), on_delete=models.CASCADE)
    gameSchedule = models.ForeignKey(GameSchedule, related_name=("betItem"), on_delete=models.CASCADE)
    transactionDate = models.DateField()
    isDeleted = models.BooleanField(default=False)
    
    def __str__(self):
        """Unicode representation of BetItem."""
        return "<BetItem Id: {self.id}>"
