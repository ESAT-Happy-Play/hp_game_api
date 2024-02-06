from rest_framework import serializers
from game.models import GameDrawType

class GameDrawTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = GameDrawType
		fields = '__all__'
		
class GameDrawTypeCreateSerializer(GameDrawTypeSerializer):
  class Meta:
    model = GameDrawType
    exclude = ('isDeleted', "gameDrawTypeName")

class GameDrawTypeUpdateSerializer(GameDrawTypeSerializer):
	class Meta:
		model = GameDrawType
		exclude = ('companyId',)
