from rest_framework import serializers
from game.models import CompanyGame, GameSchedule
from .game_schedule import GameScheduleSerializer
from .game_settings import GameSettingsSerializer, StoreSettingsSerializer

class BaseCompanyGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyGame
        fields = '__all__'

        
class CompanyGameCreateSerializer(BaseCompanyGameSerializer):
    gameSettings = GameSettingsSerializer()
    storeSettings = StoreSettingsSerializer(required=False)
    class Meta:
        model = CompanyGame
        exclude = ('isDeleted',)

class CompanyGameUpdateSerializer(BaseCompanyGameSerializer):
    class Meta:
        model = CompanyGame
        exclude = ('companyId', 'game')

        
class CompanyGameListSerializer(BaseCompanyGameSerializer):
    gameId = serializers.IntegerField(source='game.id')
    game = serializers.CharField(source='game.name')
    class Meta:
        model = CompanyGame
        fields=('id','companyId','livestream','game','gameId', 'isDeleted')