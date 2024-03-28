from game.serializers import PrizePoolSerializer, PrizePoolCreateSerializer
from game.models import PrizePool
from .base_viewset import BaseViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import action
from django.http import JsonResponse
from rest_framework import status

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