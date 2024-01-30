from game.serializers import GameDrawTypeSerializer
from game.models import GameDrawType
from .base_viewset import BaseViewSet
from rest_framework import viewsets, status
from django.http import JsonResponse

class GameDrawTypeViewSet(BaseViewSet):
    queryset = GameDrawType.objects.filter(isDeleted=False)
    serializer_class = GameDrawTypeSerializer
