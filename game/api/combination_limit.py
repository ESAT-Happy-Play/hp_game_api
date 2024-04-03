from game.serializers import CombinationLimitSerializer, CurrentCombinationCheckSerializer
from game.models import CombinationLimit, CompanyGame, BetItem
from .base_viewset import BaseViewSet
from drf_spectacular.utils import extend_schema
from django.http import JsonResponse
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.db.models import Sum, Count

class CombinationLimitViewSet(BaseViewSet):
    queryset = CombinationLimit.objects.all()
    serializer_class = CombinationLimitSerializer

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

        list_of_limits = CombinationLimit.objects.filter(companyGame=company_game, combination__in=combinations).all()
        list_of_combinations = BetItem.objects.filter(companyGame=company_game, value__in=combinations)
        combination_sums = list_of_combinations.values('value').annotate(total_amount=Sum('amount'), combinationBet=Count('value')).all()

        list_of_limits_dict = {}
        combination_sums_dict = {}
        for limit in  list_of_limits:
            list_of_limits_dict[limit.combination] = limit.limit

        for combination in  combination_sums:
            combination_sums_dict[combination['value']] = combination['combinationBet']

        total_amount = sum([combination['total_amount'] for combination in combination_sums])

        response_combination = [
            {
            "combination": combination,
            "combinationLimit": list_of_limits_dict.get(combination, None),
            "combinationBet": combination_sums_dict.get(combination, 0) if list_of_limits_dict.get(combination, None) else None
            } for combination in combinations]

        response_body = {
            "betAmountLimit": company_game.gameSettings['betLimits']['betAmountLimit'],
            "gameBets": total_amount,
            "combinations": response_combination
        }
        
        return JsonResponse(response_body, status=status.HTTP_200_OK)