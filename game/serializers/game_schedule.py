from rest_framework import serializers
from game.models import GameSchedule
from .game_draw_type import GameDrawTypeSerializer

class GameScheduleSerializer(serializers.ModelSerializer):
	gameDrawType = GameDrawTypeSerializer(read_only=True)
	class Meta:
		model = GameSchedule
		fields = '__all__'

class GameScheduleCreateSerializer(GameScheduleSerializer):
  class Meta:
    model = GameSchedule
    exclude = ('openSchedule', 'endCutOff', 'isDeleted')