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
		