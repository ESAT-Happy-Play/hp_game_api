from rest_framework import serializers
from game.models import CombinationLimit

class CombinationLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = CombinationLimit
        fields = '__all__'


class CurrentCombinationCheckSerializer(serializers.Serializer):
    combinations = serializers.StringRelatedField(many=True)
    companyGameId = serializers.IntegerField()

class CombinationLimitListPaginationSerializer(serializers.Serializer):
    companyGameId = serializers.IntegerField(required=True)
    combinations = serializers.ListField(child=serializers.CharField(max_length=20), required=False, default=[])
    size = serializers.IntegerField(required=False, default=20)
    start = serializers.IntegerField(required=False, default=0)

class CombinationLimitGameSchedBetsSerializer(serializers.Serializer):
    gameScheduleId = serializers.IntegerField(required=True)
    combinations = serializers.ListField(child=serializers.CharField(max_length=20), required=False, default=[])
