from rest_framework import serializers
from game.models import DrawResultWinner

class DrawResultWinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrawResultWinner
        fields = '__all__'

    