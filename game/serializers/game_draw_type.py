from rest_framework import serializers
from game.models import GameDrawType

class GameDrawTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = GameDrawType
		fields = '__all__'