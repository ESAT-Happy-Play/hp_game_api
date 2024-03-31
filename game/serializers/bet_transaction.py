from rest_framework import serializers
from game.models import BetTransaction, BetItem, CompanyGame, GameSchedule
from .bet_item import BetItemTransactionCreateSerializer, BetItemSerializer

class BetTransactionSerializer(serializers.ModelSerializer):
    betItems = BetItemSerializer(read_only=True, many=True)
    class Meta:
        model = BetTransaction
        fields = '__all__'

		
class BetTransactionCreateSerializer(BetTransactionSerializer):
    betItems = BetItemTransactionCreateSerializer(many=True)
    class Meta:
        model = BetTransaction
        fields = ('betItems', 'totalAmount','dateOfTransaction','accountId','betType','numberOfBets',)

    def create(self, validated_data):
        betItem_data = validated_data.pop('betItems')
        betTransaction = BetTransaction.objects.create(**validated_data)
        betItemsList = [BetItem(**item,transactionDate=validated_data["dateOfTransaction"],
                betTransaction=betTransaction) for item in betItem_data]
        betItems = BetItem.objects.bulk_create(betItemsList)
        return BetTransactionSerializer(betTransaction).data
    

class BetTransactionPageListSerializer(BetTransactionSerializer):
    class Meta:
        model = BetTransaction
        fields = ('id', 'betItems', 'totalAmount','dateOfTransaction','accountId','betType','transactionNumber', 'numberOfBets')

class TransactionPaginationSerializer(serializers.Serializer):
    size = serializers.IntegerField()
    start = serializers.IntegerField()
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    accountId = serializers.IntegerField(required=False)