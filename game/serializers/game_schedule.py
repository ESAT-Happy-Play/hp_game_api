from rest_framework import serializers
from game.models import GameSchedule
from datetime import datetime

class GameScheduleSerializer(serializers.ModelSerializer):
	class Meta:
		model = GameSchedule
		fields = '__all__'

class GameScheduleCreateSerializer(GameScheduleSerializer):
  class Meta:
    model = GameSchedule
    exclude = ('openSchedule', 'endCutOff', 'isDeleted')

class GameScheduleBetsSerializer(GameScheduleSerializer):
  openForBetting = serializers.SerializerMethodField('isOpen')

  def isOpen(self, obj):
      current_time = datetime.now().time()
      return obj.endCutOff > current_time
  class Meta:
    model = GameSchedule
    fields = ('companyId', 'date', 'openSchedule', 'endCutOff', 'status', 'gameDrawType', 'companyGame', 'openForBetting')