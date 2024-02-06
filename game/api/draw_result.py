from game.serializers import DrawResultSerializer, DrawResultCreateSerializer
from .draw_result_winner import DrawResultWinnerViewSet
from game.models import DrawResult, BetItem, PrizePool, GameSchedule, CompanyGame
from drf_spectacular.utils import extend_schema
from .base_viewset import BaseViewSet
from django.http import JsonResponse
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from dotenv import load_dotenv
import os
import requests

load_dotenv(override=True)


class DrawResultViewSet(BaseViewSet):
    queryset = DrawResult.objects.filter(isDeleted=False)
    serializer_class = DrawResultSerializer

    @extend_schema(request=DrawResultCreateSerializer)
    def create(self, request):
        
        #searching winners
        winner_view = DrawResultWinnerViewSet()
        game_schedule = get_object_or_404(GameSchedule, pk=request.data['gameSchedule'], isDeleted=False)
        company_game = get_object_or_404(CompanyGame, pk=game_schedule.companyGame.id, isDeleted=False)
        bets = BetItem.objects.filter(isDeleted=False, gameSchedule=game_schedule).all()
        winner_list = bets.filter(value=request.data['result']).all()
        request.data['noOfWinners'] = len(winner_list)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        for winner in winner_list:
            win_amount=0
            if company_game.gameSettings["isRegular"]:
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

        if 'quasiWinner' in company_game.gameSettings and company_game.gameSettings['quasiWinner'] == True:
            result_digits = sorted(request.data['result'].split('-'))
            
            quasi_winners = [bet for bet in bets if bet.bet_list() == result_digits]

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

        #broadcasting winners
        requests.post(url=os.environ.get("SOCKET_SERVICE_URL")+"draw-result", data=request.data['result'])


        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)