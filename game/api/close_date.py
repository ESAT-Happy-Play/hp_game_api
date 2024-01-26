from game.serializers import CloseDateSerializer
from game.models import CloseDate, GameDrawType
from .base_viewset import BaseViewSet
from rest_framework import viewsets, status
from django.http import JsonResponse

class CloseDateViewSet(BaseViewSet):
    queryset = CloseDate.objects.filter(isDeleted=False)
    serializer_class = CloseDateSerializer
