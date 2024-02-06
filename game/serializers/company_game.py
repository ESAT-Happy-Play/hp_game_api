from rest_framework import serializers
from game.models import CompanyGame, GameSchedule
from .game_schedule import GameScheduleSerializer

class CompanyGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyGame
        fields = '__all__'

        
class CompanyGameCreateSerializer(CompanyGameSerializer):
    class Meta:
        model = CompanyGame
        exclude = ('isDeleted',)