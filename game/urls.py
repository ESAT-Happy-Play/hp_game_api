from django.urls import path, include
from game.api import CompanyGameViewSet
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'company-game', CompanyGameViewSet, basename='company-game')