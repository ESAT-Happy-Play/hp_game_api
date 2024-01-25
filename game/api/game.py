from game.serializers import GameSerializer
from game.models import Game
from .base_viewset import BaseViewSet
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

class GameViewSet(BaseViewSet):
  queryset = Game.objects.filter(isDeleted=False)
  serializer_class = GameSerializer

  @swagger_auto_schema(
      request_body=GameSerializer,
      responses={status.HTTP_201_CREATED: GameSerializer}
  )
  def create(self, request):
      """
      Create a new Game instance.

      Parameters:
        - name: name
          type: string
          required: true
          description: The name of the game.
        - name: gameMechanics
          type: object
          required: false
          description: The game mechanics.
        - name: isDeleted
          type: boolean
          required: false
          description: Whether the game is deleted or not.

      Returns:
        201 Created - Successful response with the created instance.
      """
      return super().create(request)