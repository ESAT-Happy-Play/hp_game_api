from rest_framework import serializers
from game.models import GameDrawType

class GameDrawTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = GameDrawType
		fields = '__all__'
<<<<<<< HEAD
		
class GameDrawTypeCreateSerializer(GameDrawTypeSerializer):
  class Meta:
    model = GameDrawType
    exclude = ('isDeleted', "gameDrawTypeName")
=======

class GameDrawTypeUpdateSerializer(GameDrawTypeSerializer):
	class Meta:
		model = GameDrawType
		exclude = ('companyId',)
>>>>>>> 79608a31747f3b929a3fad2e112f247373e0dd84
