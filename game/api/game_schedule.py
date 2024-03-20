from game.serializers import GameScheduleSerializer, GameScheduleCreateSerializer
from game.models import GameSchedule, BetItem, GameDrawType
from .base_viewset import BaseViewSet
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum
from drf_spectacular.utils import extend_schema, OpenApiParameter
import uuid
from django.db.models import Max
from datetime import datetime, timedelta

class GameScheduleViewSet(BaseViewSet):
    queryset = GameSchedule.objects.all()
    active_queryset = queryset.filter(isDeleted=False)
    serializer_class = GameScheduleSerializer

    @extend_schema(parameters=[
        OpenApiParameter(name='companyId', description='companyId filter', type=str),
        OpenApiParameter(name='includeIsDeleted', description='isDeleted filter', type=bool)
    ])
    def list(self, request):
        queryset = self.queryset
        company_id = self.request.query_params.get('companyId', None)
        include_is_deleted = request.query_params.get('includeIsDeleted', 'true').lower() == 'true'

        if company_id:
            try:
                company_id = uuid.UUID(company_id)
                queryset = queryset.filter(companyGame__companyId__exact=company_id)
            except ValueError:
                return JsonResponse({"error": "Invalid UUID format for companyId"}, status=status.HTTP_400_BAD_REQUEST)

        if not include_is_deleted:
            queryset = queryset.filter(isDeleted=False)

        serializer = self.serializer_class(queryset, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

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
        game_schedule = get_object_or_404(self.active_queryset, pk=pk)
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
        game_schedule = get_object_or_404(self.active_queryset, pk=pk)
        bet_items = BetItem.objects.filter(gameSchedule=game_schedule, isDeleted=False)
        total_amount = bet_items.aggregate(Sum('amount'))['amount__sum'] or 0

        data = {'total_bet_amount': total_amount}
        return JsonResponse(data, status=status.HTTP_200_OK)

    @extend_schema(parameters=[
        OpenApiParameter(name='companyId', description='company id', type=str),
        OpenApiParameter(name='gameDrawType', description='game draw type id', type=int),
        OpenApiParameter(name='companyGame', description='company game id', type=int),
    ],
    operation_id='latest-game-schedule')
    @action(detail=False, methods=['get'], url_path='latest-date')
    def latest_date(self, request):
        """
        Get the latest game schedule date for a given companyId, gameDrawType, and companyGame.
        """
        company_id = request.query_params.get('companyId')
        game_draw_type_id = request.query_params.get('gameDrawType')
        company_game_id = request.query_params.get('companyGame')

        if not all([company_id, game_draw_type_id, company_game_id]):
            return JsonResponse({"error": "companyId, gameDrawType, and companyGame are required parameters"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            company_id = uuid.UUID(company_id)
            game_draw_type_id = int(game_draw_type_id)
            company_game_id = int(company_game_id)
        except ValueError:
            return JsonResponse({"error": "Invalid UUID or integer format for parameters"}, status=status.HTTP_400_BAD_REQUEST)

        latest_date = GameSchedule.objects.filter(
            companyId=company_id,
            gameDrawType_id=game_draw_type_id,
            companyGame_id=company_game_id,
            isDeleted=False
        ).aggregate(latest_date=Max('date'))['latest_date']

        if latest_date is None:
            # return yesterday as last schedule
            today = datetime.now()
            yesterday = today - timedelta(days=1)
            formatted_yesterday = yesterday.strftime('%Y-%m-%d') # format the date as 'YYYY-MM-DD'
            data = {'latest_date': formatted_yesterday}
            return JsonResponse(data, status=status.HTTP_200_OK)

        data = {'latest_date': latest_date}
        return JsonResponse(data, status=status.HTTP_200_OK)
