from rest_framework import serializers
from game.models import GameSchedule

class GameScheduleSerializer(serializers.ModelSerializer):
	class Meta:
		model = GameSchedule
		fields = '__all__'