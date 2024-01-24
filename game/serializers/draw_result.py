from rest_framework import serializers
from game.models import DrawResult

class DrawResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrawResult
        fields = '__all__'

    