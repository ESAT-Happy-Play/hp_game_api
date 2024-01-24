from django.urls import path, include
from game.api import CompanyGameViewSet, DrawResultViewSet, DrawResultWinnerViewSet
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'company-game', CompanyGameViewSet, basename='company-game')
router.register(r'draw-result', DrawResultViewSet, basename='draw-result')
router.register(r'draw-result-winner', DrawResultWinnerViewSet, basename='draw-result-winner')