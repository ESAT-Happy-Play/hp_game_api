from rest_framework import serializers
from game.models import PrizePool

class PrizePoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrizePool
        fields = '__all__'

    