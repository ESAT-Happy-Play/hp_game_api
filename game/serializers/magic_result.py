from rest_framework import serializers
from game.models import MagicResult
from .draw_result_winner import DrawResultWinnerSerializer

class MagicResultSerializer(serializers.ModelSerializer):
    winners = DrawResultWinnerSerializer(read_only=True, many=True, source='drawResultWinner')
    class Meta:
        model = MagicResult
        fields = '__all__'

class MagicResultCreateSerializer(MagicResultSerializer):
  class Meta:
    model = MagicResult
    exclude = ('noOfWinners', 'isDeleted', 'noOfQuasiWinners', 'amount')

class MagicResultListSerializer(serializers.ModelSerializer):
  winners = DrawResultWinnerSerializer(read_only=True, many=True, source='drawResultWinner')
  class Meta:
    model = MagicResult
    fields = ['id', 'companyId', 'result', 'amount', 'noOfWinners', 'noOfQuasiWinners', 'companyGame', 'gameSchedule','winners']

class MagicResultListPaginationSerializer(serializers.Serializer):
    companyId = serializers.IntegerField(required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    size = serializers.IntegerField(required=False, default=10)
    start = serializers.IntegerField(required=False, default=0)
