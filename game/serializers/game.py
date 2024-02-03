from rest_framework import serializers
from game.models import Game

class GameSerializer(serializers.ModelSerializer):
	class Meta:
		model = Game
		fields = '__all__'
		
        
class GameCreateSerializer(GameSerializer):
    class Meta:
        model = Game
        exclude = ('isDeleted',)