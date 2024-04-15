from rest_framework import serializers
from game.models import DrawResultWinner

class DrawResultWinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrawResultWinner
        fields = '__all__'

class DrawResultWinnerCreateSerializer(DrawResultWinnerSerializer):
    class Meta:
        model = DrawResultWinner
        exclude = ('isDeleted',)

class DrawResultWinnerUpdateSerializer(DrawResultWinnerSerializer):
    class Meta:
        model = DrawResultWinner
        fields = ('isCreditProcessed',)
        
class DrawResultWinnerPaginationSerializer(serializers.Serializer):
    companyGameId = serializers.IntegerField(required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    size = serializers.IntegerField(required=False, default=10)
    start = serializers.IntegerField(required=False, default=0)
