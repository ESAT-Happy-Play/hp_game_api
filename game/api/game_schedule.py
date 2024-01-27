from game.serializers import GameScheduleSerializer
from game.models import GameSchedule, BetItem
from .base_viewset import BaseViewSet
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db.models import Count

class GameScheduleViewSet(BaseViewSet):
    queryset = GameSchedule.objects.filter(isDeleted=False)
    serializer_class = GameScheduleSerializer

    @action(detail=True, methods=['get'])
    def combination_percentage(self, request, pk=None):
        """
        Get the combination percentage of the draw given gameScheduleId.
        """
        game_schedule = get_object_or_404(self.queryset, pk=pk)
        bet_items = BetItem.objects.filter(gameSchedule=game_schedule)
        total_unique_values = bet_items.values('value').distinct().count()
        company_game = game_schedule.companyGame
        unique_combinations = company_game.gameSettings.get('unique_combinations', 0) # should have unique_combinations on the gameSettings JSONB data

        # calculate the combination percentage
        if unique_combinations == 0: # no bets scenario
          combination_percentage = 0
        else:
          combination_percentage = (total_unique_values / unique_combinations) * 100

        data = {'combination_percentage': combination_percentage}
        return JsonResponse(data, status=status.HTTP_200_OK)
