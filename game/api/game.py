from game.serializers import GameSerializer, GameCreateSerializer
from game.models import Game
from .base_viewset import BaseViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.http import JsonResponse
import random

class GameViewSet(BaseViewSet):
  queryset = Game.objects.all()
  active_queryset = queryset.filter(isDeleted=False)
  serializer_class = GameSerializer

  @extend_schema(request=GameCreateSerializer)
  def create(self, request):
    return super().create(request)

  @extend_schema(parameters=[
        OpenApiParameter(name='numPicks', description='number of lucky-pick/s to generate (default is 1)', type=int),
    ])
  @action(detail=True, methods=["get"], url_path="lucky-pick")
  def get_game_lucky_pick(self, request, pk=None):
      # NOTE: this is just the initial lucky pick logic, the lucky pick process is not a straight forward random picking but has its own business logic
      game = get_object_or_404(self.active_queryset, pk=pk)
      serializer = GameSerializer(game)
      game_data = serializer.data
      game_mechanics = game_data.get('gameMechanics')

      n_cards = game_mechanics.get('nCards')
      n_suites = game_mechanics.get('nSuites')

      cards = ["A", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
      suites = ["H", "S", "D", "C"]

      number_of_picks = int(request.query_params.get('numPicks', 1))

      lucky_picks = []
      for _ in range(number_of_picks):
          random_cards = '-'.join(random.choices(cards, k=n_cards))
          if n_suites is not None and n_suites != 0:
              random_suites = '-'.join(random.choices(suites, k=n_suites))
              lucky_pick = f"{random_cards}-{random_suites}"
          else:
              lucky_pick = random_cards
          lucky_picks.append(lucky_pick)

      return JsonResponse({"gameId": pk, "luckyPicks": lucky_picks}, status=status.HTTP_200_OK)