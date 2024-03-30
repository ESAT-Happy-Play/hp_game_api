from game.serializers import DrawResultSerializer, DrawResultCreateSerializer, GameScheduleSerializer
from .draw_result_winner import DrawResultWinnerViewSet
from game.models import DrawResult, BetItem, PrizePool, GameSchedule, CompanyGame
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

    @action(detail=False, methods=['get'], url_path='schedule/(?P<gameScheduleId>[^/.]+)')
    def draw_result_get_by_schedule(self, request, gameScheduleId=None):
        queryset = self.queryset
        if gameScheduleId:
            queryset = queryset.filter(gameSchedule__exact=gameScheduleId)

        serializer = DrawResultSerializer(queryset, many=True)
        return JsonResponse(serializer.data[0] if serializer.data else {}, status=status.HTTP_200_OK)
        
    @extend_schema(request=DrawResultCreateSerializer)
    def create(self, request):
        
        #searching winners
        winner_view = DrawResultWinnerViewSet()
        game_schedule = get_object_or_404(GameSchedule, pk=request.data['gameSchedule'], isDeleted=False)
        company_game = get_object_or_404(CompanyGame, pk=game_schedule.companyGame.id, isDeleted=False)

        #finding of winners
        bets = BetItem.objects.filter(isDeleted=False, gameSchedule=game_schedule).all()
        winner_list = bets.filter(value=request.data['result']).all()

        if company_game.gameSettings['prizeCalculation']['enableQuasi'] == True:
            result_digits = sorted(request.data['result'].split('-'))
            
            quasi_winners = [bet for bet in bets.exclude(value=request.data['result']) if bet.bet_list() == result_digits]
        else:
          quasi_winners = []

        request.data['noOfWinners'] = len(winner_list)
        request.data['noOfQuasiWinners'] = len(quasi_winners)


        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()


        #creation of winner entities
        for winner in winner_list:
            win_amount=0
            if 'winningMult' in company_game.gameSettings["prizeCalculation"]:
                win_amount=winner.amount*company_game.gameSettings["winningMult"]

            else:
                prize_pool = get_object_or_404(PrizePool, gameSchedule=game_schedule, isDeleted=False)
                win_amount = prize_pool.winningPrize/len(winner_list)
            
            new_request = HttpRequest()
            new_request.data = {
                "drawResult":serializer.data['id'],
                "accountInfoId":winner.betTransaction.accountId,
                "betInfo":winner.id,
                "amount":win_amount,
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