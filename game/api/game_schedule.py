from game.serializers import GameScheduleSerializer, GameDrawTypeSerializer
from game.models import GameSchedule
from .base_viewset import BaseViewSet
from rest_framework.decorators import action
from datetime import datetime
from django.http import JsonResponse
from rest_framework import status

class GameScheduleViewSet(BaseViewSet):
    queryset = GameSchedule.objects.filter(isDeleted=False)
    serializer_class = GameScheduleSerializer

    @action(detail=False, methods=["get"], url_path="<int:companyGameId>/bets/current")
    def get_bet_current(self,request, companyGameId=None):
        current_time = datetime.now().time()
        current_date = datetime.now().date()
        types = [e.gameDrawType for e in self.queryset.filter(date=current_date, companyGame=companyGameId)]
        type = [e for e in types if e.openSchedule <= current_time].sort(key=lambda t: t.openSchedule)
        serializer = GameDrawTypeSerializer(data=type)
        serializer.is_valid(raise_exception=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)