from game.serializers import GameScheduleSerializer
from game.models import GameSchedule
from .base_viewset import BaseViewSet

class GameScheduleViewSet(BaseViewSet):
    queryset = GameSchedule.objects.filter(isDeleted=False)
    serializer_class = GameScheduleSerializer
