from rest_framework import serializers
from game.models import BetItem

class BetItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = BetItem
		fields = '__all__'

		
class BetItemCreateSerializer(BetItemSerializer):
    class Meta:
        model = BetItem
        exclude = ('isDeleted',)
        
class BetItemTransactionCreateSerializer(BetItemSerializer):
    class Meta:
        model = BetItem
        exclude = ('isDeleted','betTransaction','transactionDate')
		
class BetItemListPaginationSerializer(serializers.Serializer):
    companyId = serializers.IntegerField(required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    size = serializers.IntegerField(required=False, default=10)
    start = serializers.IntegerField(required=False, default=0)
