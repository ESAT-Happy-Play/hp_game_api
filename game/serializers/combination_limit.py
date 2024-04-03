from rest_framework import serializers
from game.models import CombinationLimit

class CombinationLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = CombinationLimit
        fields = '__all__'


class CurrentCombinationCheckSerializer(serializers.Serializer):
    combinations = serializers.StringRelatedField(many=True)
    companyGameId = serializers.IntegerField()

