from game.serializers import CombinationLimitSerializer, CurrentCombinationCheckSerializer, CombinationLimitListPaginationSerializer, CombinationLimitGameSchedBetsSerializer
from game.models import CombinationLimit, CompanyGame, BetItem
from .base_viewset import BaseViewSet
from drf_spectacular.utils import extend_schema
from django.http import JsonResponse
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.db.models import Sum, Count
from drf_spectacular.utils import extend_schema, OpenApiParameter
import uuid

class CombinationLimitViewSet(BaseViewSet):
    queryset = CombinationLimit.objects.all()
    serializer_class = CombinationLimitSerializer
    
    @extend_schema(parameters=[OpenApiParameter(name='companyId', description='CompanyId from core service', type=str, location=OpenApiParameter.PATH, required=True)], operation_id='get_combination_limit')
    @action(detail=False, methods=["get"], url_path="(?P<companyId>[^/.]+)/list")
    def get_combination_limit(self, request, companyId=None):
        try:
            company_id = uuid.UUID(companyId)
            queryset = self.queryset.filter(companyId__exact=company_id)
        except ValueError:
            return JsonResponse({"error": "Invalid UUID format for companyId"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CombinationLimitSerializer(queryset, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

    @extend_schema(request=CombinationLimitSerializer)
    def update(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = CombinationLimitSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)



    @extend_schema(request=CurrentCombinationCheckSerializer)
    @action(detail=False, methods=['post'], url_path='current-limit')
    def check_current_limit(self, request):
        combinations = request.data['combinations']
        company_game =  get_object_or_404(CompanyGame, pk=request.data['companyGameId'])
        gameScheduleId = request.data['gameScheduleId']

        list_of_limits = CombinationLimit.objects.filter(companyGame=company_game, combination__in=combinations).all()
        limit_query = BetItem.objects.filter(companyGame=company_game, gameSchedule=gameScheduleId)
        
        list_of_combinations = limit_query.filter(value__in=combinations)
        combination_sums = list_of_combinations.values('value').annotate(total_amount=Sum('amount'), combinationBet=Count('value')).all()
        bet_Amounts = limit_query.values('value').annotate(total_amount=Sum('amount')).all()

        list_of_limits_dict = {}
        combination_sums_dict = {}
        for limit in  list_of_limits:
            list_of_limits_dict[limit.combination] = limit.limit

        for combination in  combination_sums:
            combination_sums_dict[combination['value']] = combination['total_amount']

        total_amount = sum([betAmount['total_amount'] for betAmount in bet_Amounts])

        response_combination = [
            {
            "combination": combination,
            "combinationLimit": list_of_limits_dict.get(combination, None),
            "combinationBet": combination_sums_dict.get(combination, 0),
            "hasCombinationLimit": list_of_limits_dict.get(combination, 0) > 0 if list_of_limits_dict.get(combination, False) else False
            } for combination in combinations]

        response_body = {
            "betAmountLimit": company_game.gameSettings['betLimits']['betAmountLimit'],
            "gameBets": total_amount,
            "combinations": response_combination
        }
        
        return JsonResponse(response_body, status=status.HTTP_200_OK)

    @extend_schema(request=CombinationLimitListPaginationSerializer)
    @action(detail=False, methods=['post'], url_path='list')
    def get_paginated_combination_limit(self, request):
        company_game_id = request.data.get('companyGameId')
        start = 0
        size = 20
            
        if 'start' in request.data:
            start = request.data.get('start')

        if 'size' in request.data:
            size = request.data.get('size')

        if 'combinations' in request.data:
            combinations = request.data.get('combination')

        if combinations:
            new_queryset = self.queryset.filter(companyGame=company_game_id, combination__in=combinations)
        else:
            new_queryset = self.queryset.filter(companyGame=company_game_id)

        total = new_queryset.count()
        data = new_queryset[start:start+size]
        serializer = self.serializer_class(data, many=True)

        page_offset = (start+size)

        if page_offset >= total:
            page_offset = 0

        response_body = {
            "count": start + size,
            "offset": page_offset,
            "totalCount": total,
            "combinations": serializer.data
        }

        return JsonResponse(response_body, status=status.HTTP_200_OK)

    @extend_schema(request=CombinationLimitGameSchedBetsSerializer)
    @action(detail=False, methods=['post'], url_path='gameschedule-bets')
    def get_total_bet_per_schedule(self, request):
        game_schedule_id = request.data.get('gameScheduleId')
        combinations = request.data.get('combinations', None)

        bets = BetItem.objects.filter(gameSchedule=game_schedule_id)
        if combinations:
            bets = bets.filter(value__in=combinations)

        combination_sums = bets.values('value').annotate(totalAmountBet=Sum('amount')).all()

        combination_bets = [
            {
                'combination': combination['value'],
                'totalAmountBet': combination['totalAmountBet'],
            }
            for combination in combination_sums
        ]

        response_body = {
            "gameScheduleId": game_schedule_id,
            "combinationBets": combination_bets
        }

        return JsonResponse(response_body, status=status.HTTP_200_OK)