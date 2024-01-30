from rest_framework import serializers
from game.models import GameSchedule
from .game_draw_type import GameDrawTypeSerializer

class GameScheduleSerializer(serializers.ModelSerializer):
	gameDrawTypeDetail = GameDrawTypeSerializer(source="gameDrawType", read_only=True)
	class Meta:
		model = GameSchedule
		fields = '__all__'