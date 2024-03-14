from rest_framework import serializers
from game.models import WinStreak

class WinStreakSerializer(serializers.ModelSerializer):
	class Meta:
		model = WinStreak
		fields = '__all__'
		