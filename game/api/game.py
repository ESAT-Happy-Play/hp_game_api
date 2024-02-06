from game.serializers import GameSerializer, GameCreateSerializer
from game.models import Game
from .base_viewset import BaseViewSet
from drf_spectacular.utils import extend_schema

class GameViewSet(BaseViewSet):
  queryset = Game.objects.filter(isDeleted=False)
  serializer_class = GameSerializer

  @extend_schema(request=GameCreateSerializer)
  def create(self, request):
    return super().create(request)