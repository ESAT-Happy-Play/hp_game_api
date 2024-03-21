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
    companyGame= serializers.IntegerField()
    gameSchedule= serializers.IntegerField()
    class Meta:
        model = BetTransaction
        fields = ('betItems', 'totalAmount','dateOfTransaction','accountId','betType','companyGame','gameSchedule', 'transactionNumber', 'numberOfBets')

    def create(self, validated_data):
        betItem_data = validated_data.pop('betItems')
        company_game = CompanyGame.objects.filter(pk=validated_data.pop('companyGame')).first()
        game_schedule = GameSchedule.objects.filter(pk=validated_data.pop('gameSchedule')).first()
        betTransaction = BetTransaction.objects.create(**validated_data)
        betItemsList = [BetItem(**item,transactionDate=validated_data["dateOfTransaction"],
                betTransaction=betTransaction, gameSchedule=game_schedule, companyGame=company_game) for item in betItem_data]
        betItems = BetItem.objects.bulk_create(betItemsList)
        return BetTransactionSerializer(betTransaction).data
    

class BetTransactionPageListSerializer(BetTransactionSerializer):
    class Meta:
        model = BetTransaction
        fields = ('betItems', 'totalAmount','dateOfTransaction','accountId','betType','transactionNumber', 'numberOfBets')

class TransactionPaginationSerializer(serializers.Serializer):
    size = serializers.IntegerField()
    start = serializers.IntegerField()