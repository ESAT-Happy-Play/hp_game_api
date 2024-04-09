from game.serializers import DrawResultSerializer, DrawResultCreateSerializer, GameScheduleSerializer, DrawResultListSerializer, DrawResultListPaginationSerializer
from .draw_result_winner import DrawResultWinnerViewSet
from game.models import DrawResult, BetItem, PrizePool, GameSchedule, CompanyGame, WinStreak
from drf_spectacular.utils import extend_schema
from .base_viewset import BaseViewSet
from django.http import JsonResponse
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from dotenv import load_dotenv
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import action
import os
import requests

load_dotenv(override=True)


class DrawResultViewSet(BaseViewSet):
    queryset = DrawResult.objects.filter(isDeleted=False)
    serializer_class = DrawResultSerializer


    @extend_schema(parameters=[OpenApiParameter(name='includeIsDeleted', description='isDeleted filter', type=bool)])
    def list(self, request):
        include_is_deleted = request.query_params.get('includeIsDeleted', 'true').lower() == 'true'
        queryset = self.queryset.prefetch_related('drawResultWinner').all()

        if not include_is_deleted:
            queryset = self.queryset.filter(isDeleted=False)

        serializer = DrawResultListSerializer(queryset, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

    @extend_schema(parameters=[
        OpenApiParameter(name='gameScheduleId', description='Game Schedule ID', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    operation_id='draw_result_get_by_schedule')
    @action(detail=False, methods=['get'], url_path='(?P<gameScheduleId>[^/.]+)/game-schedule')
    def draw_result_get_by_schedule(self, request, gameScheduleId=None):
        draw_result = self.queryset.filter(gameSchedule__exact=gameScheduleId).first()

        if draw_result is None:
            return JsonResponse({'detail': 'No Draw result found for the specified game schedule ID.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(draw_result)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    
    
    @extend_schema(parameters=[
        OpenApiParameter(name='gameScheduleIds', description='Game Schedule ID', type=str, location=OpenApiParameter.PATH, required=True),
    ],
    operation_id='draw_result_get_by_schedule_list')
    @action(detail=False, methods=['get'], url_path='game-schedule/list')
    def draw_result_get_by_schedule_list(self, request):
        draw_result_query = self.queryset
        
        if 'gameScheduleIds' in request.query_params:
            draw_result_query = draw_result_query.filter(gameSchedule__in=request.query_params.get('gameScheduleIds').split(','))

        serializer = self.serializer_class(draw_result_query, many=True)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        
        
    @extend_schema(request=DrawResultCreateSerializer)
    def create(self, request):
        winner_view = DrawResultWinnerViewSet()
        game_schedule = get_object_or_404(GameSchedule, pk=request.data['gameSchedule'], isDeleted=False)
        company_game = get_object_or_404(CompanyGame, pk=game_schedule.companyGame.id, isDeleted=False)
        prize_calculation = company_game.gameSettings["prizeCalculation"]

        #finding of winners
        bets = BetItem.objects.filter(isDeleted=False, gameSchedule=game_schedule).all()
        winner_list = bets.filter(value=request.data['result']).all()

        #finding quasi winners
        if prize_calculation['enableQuasi'] == True:
            result_digits = sorted(request.data['result'].split('-'))
            
            quasi_winners = [bet for bet in bets.exclude(value=request.data['result']) if bet.bet_list() == result_digits]
        else:
          quasi_winners = []
        
        #prize_calculation
        win_amount = 0
        isPool = False
        if 'consecutiveWins' in prize_calculation:
            streak = WinStreak.objects.filter(accountId__in=[winners.betTransaction.accountId for winners in winner_list]).all()
            print(streak)
            if [match for match in streak if match.streak == prize_calculation['consecutiveWins']]:
                prizepool = PrizePool.objects.filter(gameSchedule=game_schedule).first()
                win_amount = prizepool.winningPrize
                isPool = True

            else:
                win_amount = (sum([winners.amount for winners in winner_list]) * prize_calculation['winningMultiplier']['winPerBet'])

        else:
            if 'winningMultiplier' in prize_calculation:
                win_amount = (sum([winners.amount for winners in winner_list]) * prize_calculation['winningMultiplier']['winPerBet'])

            elif 'pooling' in prize_calculation:
                prizepool = PrizePool.objects.filter(gameSchedule=game_schedule).first()
                win_amount = win_amount + prizepool.winningPrize
                isPool = True



        request.data['noOfWinners'] = len(winner_list)
        request.data['noOfQuasiWinners'] = len(quasi_winners)
        request.data['amount'] = win_amount + sum([item.amount for item in quasi_winners])


        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()



        #creation of winner entities
        for winner in winner_list:
            winnings = 0

            if isPool:
                winnings = win_amount/len(winner_list)

            else:
                winnings = winner.amount * prize_calculation['winningMultiplier']['winPerBet']

            new_request = HttpRequest()
            new_request.data = {
                "drawResult":serializer.data['id'],
                "accountInfoId":winner.betTransaction.accountId,
                "betInfo":winner.id,
                "amount":winnings,
                "isQuasi": False
            }
            winner_view.create(new_request)


        for quasi_winner in quasi_winners:
            quasi_request = HttpRequest()
            quasi_request.data = {
                "drawResult":serializer.data['id'],
                "accountInfoId":quasi_winner.betTransaction.accountId,
            "betInfo":quasi_winner.id,
                "amount":quasi_winner.amount,
                "isQuasi": True
            }
            winner_view.create(quasi_request)

        # game schedule data
        game_schedule_serializer = GameScheduleSerializer(game_schedule)
        serialized_game_schedule = game_schedule_serializer.data

        broadcast_body_params = {
            "gameSchedule": serialized_game_schedule,
            "value": request.data['result'],
            "enableQuasi": company_game.gameSettings['prizeCalculation']['enableQuasi']
        }

        #broadcasting winners
        requests.post(url=os.environ.get("SOCKET_SERVICE_URL")+"draw-result", json=broadcast_body_params)


        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(request=DrawResultListPaginationSerializer)
    @action(detail=False, methods=['post'], url_path='list')
    def get_paginated_draw_result_list(self, request):
        companygameId = request.data.get('companyGameId', None)
        start_date = request.data.get('start_date', None)
        end_date = request.data.get('end_date', None)
        start = request.data.get('start', 0)
        size = request.data.get('size', 10)

        draw_results = self.queryset

        if companygameId:
            draw_results = draw_results.filter(companyGame=companygameId)

        if start_date:
            draw_results = draw_results.filter(gameSchedule__date__gte=start_date)

        if end_date:
            draw_results = draw_results.filter(gameSchedule__date__lte=end_date)

        draw_results = draw_results.order_by('-gameSchedule__date')  # order by date in descending order

        total = draw_results.count()
        data = draw_results[start:start + size]

        response_data = [
            {
                'id': item.id,
                'result': item.result,
                'amount': item.amount,
                'noOfWinners': item.noOfWinners,
                'companyGame': item.companyGame_id,
                'gameSchedule': item.gameSchedule_id,
                'drawDate': item.gameSchedule.date,
                'drawTime': item.gameSchedule.drawTime,
                'noOfBets': BetItem.objects.filter(isDeleted=False, gameSchedule=item.gameSchedule).count()
            }
            for item in data
        ]

        response_body = {
            "count": start + size,
            "offset":  start + size if start + size < total else 0,
            "totalCount": total,
            "data": response_data
        }

        return JsonResponse(response_body, status=status.HTTP_200_OK)