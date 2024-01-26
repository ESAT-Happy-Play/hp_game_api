from django.urls import path, include
from game.api import *
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'company-game', CompanyGameViewSet, basename='company-game')
router.register(r'draw-result', DrawResultViewSet, basename='draw-result')
router.register(r'draw-result-winner', DrawResultWinnerViewSet, basename='draw-result-winner')
router.register(r'game', GameViewSet, basename='game')
router.register(r'closed-date', CloseDateViewSet, basename='closed-date')
router.register(r'game-draw-type', GameDrawTypeViewSet, basename='game-draw-type')
router.register(r'bet-item', BetItemViewSet, basename='bet-item')