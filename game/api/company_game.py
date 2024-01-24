from django.http import JsonResponse
from game.serializers import CompanyGameSerializer
from game.models import CompanyGame
from .base_viewset import BaseViewSet

class CompanyGameViewSet(BaseViewSet):
    queryset = CompanyGame.objects.filter(isDeleted=False)
    serializer_class = CompanyGameSerializer()
