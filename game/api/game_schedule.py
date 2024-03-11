from game.serializers import GameScheduleSerializer, GameScheduleCreateSerializer
from game.models import GameSchedule, BetItem, GameDrawType
from .base_viewset import BaseViewSet
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum
from drf_spectacular.utils import extend_schema

class GameScheduleViewSet(BaseViewSet):
    queryset = GameSchedule.objects.filter(isDeleted=False)
    serializer_class = GameScheduleSerializer

    @extend_schema(request=GameScheduleCreateSerializer)
    def create(self, request):
        game_draw_type_pk = request.data['gameDrawType']
        game_draw_type = get_object_or_404(GameDrawType, pk=game_draw_type_pk, isDeleted=False)
        request.data['openSchedule'] = game_draw_type.openSchedule
        request.data['endCutOff'] = game_draw_type.endCutOff
        return super().create(request)

    @action(detail=True, methods=['get'], url_path='combination-percentage')
    def combination_percentage(self, request, pk=None):
        """
        Get the combination percentage of the draw given gameScheduleId.
        """
        game_schedule = get_object_or_404(self.queryset, pk=pk)
        bet_items = BetItem.objects.filter(gameSchedule=game_schedule, isDeleted=False)
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

    @action(detail=True, methods=['get'], url_path='total-bet-amount')
    def total_bet_amount(self, request, pk=None):
        """
        Get total amount of bets given gameScheduleId.
        """
        game_schedule = get_object_or_404(self.queryset, pk=pk)
        bet_items = BetItem.objects.filter(gameSchedule=game_schedule, isDeleted=False)
        total_amount = bet_items.aggregate(Sum('amount'))['amount__sum'] or 0

        data = {'total_bet_amount': total_amount}
        return JsonResponse(data, status=status.HTTP_200_OK)
