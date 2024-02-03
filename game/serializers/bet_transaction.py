from rest_framework import serializers
from game.models import BetTransaction

class BetTransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = BetTransaction
		fields = '__all__'
		
		
class BetTransactionCreateSerializer(BetTransactionSerializer):
    class Meta:
        model = BetTransaction
        exclude = ('isDeleted', 'transactionNumber')