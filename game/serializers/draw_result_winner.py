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