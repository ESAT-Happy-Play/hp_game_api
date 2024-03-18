from rest_framework import serializers
from game.models import CompanyGame, GameSchedule
from .game_schedule import GameScheduleSerializer
from .game_settings import GameSettingsSerializer, StoreSettingsSerializer

class CompanyGameSerializer(serializers.ModelSerializer):
    gameSettings = GameSettingsSerializer()
    storeSettings = StoreSettingsSerializer(required=False)
    class Meta:
        model = CompanyGame
        fields = '__all__'

        
class CompanyGameCreateSerializer(CompanyGameSerializer):
    class Meta:
        model = CompanyGame
        exclude = ('isDeleted',)

class CompanyGameUpdateSerializer(CompanyGameSerializer):
    class Meta:
        model = CompanyGame
        exclude = ('companyId', 'game')