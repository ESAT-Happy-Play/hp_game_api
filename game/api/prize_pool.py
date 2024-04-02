from game.serializers import PrizePoolSerializer, PrizePoolCreateSerializer
from game.models import PrizePool, DrawResult
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

    @extend_schema(parameters=[
        OpenApiParameter(name='companyGameId', description='Company Game ID', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    operation_id='get_if_prize_pool_has_winners')
    @action(detail=False, methods=['get'], url_path='(?P<companyGameId>[^/.]+)/latest/has-winners')
    def get_if_prize_pool_has_winners(self, request, companyGameId):
        latest_prize_pool = self.queryset.filter(companyGame_id=companyGameId, isDeleted=False).order_by('-id').first()
        if latest_prize_pool is None:
            return JsonResponse({'detail': 'No prize pool found for the specified company game ID.'}, status=status.HTTP_404_NOT_FOUND)

        draw_result = DrawResult.objects.filter(gameSchedule__exact=latest_prize_pool.gameSchedule_id, isDeleted=False).first()
        if draw_result is None:
            return JsonResponse({'detail': 'No draw result yet, cannot determine if has winners.'}, status=status.HTTP_404_NOT_FOUND)

        has_winners = draw_result.noOfWinners is not None and draw_result.noOfWinners > 0

        return JsonResponse({'has_winners': has_winners}, status=status.HTTP_200_OK)