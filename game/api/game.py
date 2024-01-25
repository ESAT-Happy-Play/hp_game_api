from game.serializers import GameSerializer
from game.models import Game
from .base_viewset import BaseViewSet

class GameViewSet(BaseViewSet):
  queryset = Game.objects.filter(isDeleted=False)
  serializer_class = GameSerializer
