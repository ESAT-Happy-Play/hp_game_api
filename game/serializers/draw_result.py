from rest_framework import serializers
from game.models import DrawResult
from .draw_result_winner import DrawResultWinnerSerializer

class DrawResultSerializer(serializers.ModelSerializer):
    winners = DrawResultWinnerSerializer(read_only=True, many=True, source='drawResultWinner')
    class Meta:
        model = DrawResult
        fields = '__all__'



class DrawResultCreateSerializer(DrawResultSerializer):
  class Meta:
    model = DrawResult
    exclude = ('noOfWinners', 'isDeleted', 'noOfQuasiWinners', 'amount')

class DrawResultListSerializer(serializers.ModelSerializer):
  winners = DrawResultWinnerSerializer(read_only=True, many=True, source='drawResultWinner')
  class Meta:
    model = DrawResult
    fields = ['id', 'companyId', 'result', 'amount', 'noOfWinners', 'noOfQuasiWinners', 'companyGame', 'gameSchedule','winners']
