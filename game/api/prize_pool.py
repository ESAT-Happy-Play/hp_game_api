from game.serializers import PrizePoolSerializer, PrizePoolCreateSerializer, PrizePoolStateUpdateSerializer
from game.models import PrizePool
from .base_viewset import BaseViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import action
from django.http import JsonResponse
from rest_framework import status
from django.shortcuts import get_object_or_404

class PrizePoolViewSet(BaseViewSet):
    queryset = PrizePool.objects.filter(isDeleted=False)
    serializer_class = PrizePoolSerializer

    @extend_schema(request=PrizePoolCreateSerializer)
    def create(self, request):
        return super().create(request)

    @extend_schema(parameters=[
        OpenApiParameter(name='companyGameId', description='Company Game ID', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    operation_id='get_latest_prize_pool')
    @action(detail=False, methods=['get'], url_path='(?P<companyGameId>[^/.]+)/latest')
    def get_latest_prize_pool(self, request, companyGameId):
        latest_prize_pool = self.queryset.filter(companyGame_id=companyGameId, isDeleted=False).order_by('-id').first()

        if latest_prize_pool is None:
            return JsonResponse({'detail': 'No prize pool found for the specified company game ID.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(latest_prize_pool)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(parameters=[
        OpenApiParameter(name='gameScheduleId', description='Game Schedule ID', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    operation_id='get_prize_pool_by_game_schedule')
    @action(detail=False, methods=['get'], url_path='(?P<gameScheduleId>[^/.]+)/game-schedule')
    def get_prize_pool_by_game_schedule(self, request, gameScheduleId):
        latest_prize_pool = self.queryset.filter(gameSchedule__exact=gameScheduleId, isDeleted=False).first()

        if latest_prize_pool is None:
            return JsonResponse({'detail': 'No prize pool found for the specified game schedule ID.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(latest_prize_pool)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    
    
    @extend_schema(request=PrizePoolStateUpdateSerializer)
    @action(detail=True, methods=['patch'], url_path="update-drawn")
    def update_winners_and_drawn(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data)