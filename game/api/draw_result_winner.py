from game.serializers import DrawResultWinnerSerializer, DrawResultWinnerCreateSerializer
from game.models import DrawResultWinner, DrawResult
from .base_viewset import BaseViewSet
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from django.http import JsonResponse
from rest_framework import status

class DrawResultWinnerViewSet(BaseViewSet):
    queryset = DrawResultWinner.objects.filter(isDeleted=False)
    serializer_class = DrawResultWinnerSerializer

    @extend_schema(request=DrawResultWinnerCreateSerializer)
    def create(self, request):
        return super().create(request)

    @action(detail=False, methods=['get'], url_path='last-two-draws')
    def last_two_draws_winners(self, request):
        """
        Get winners from latest 2 draws.
        """
        two_latest_draws = DrawResult.objects.filter( isDeleted=False).order_by('-id')[:2].values_list('id', flat=True)
        two_latest_draws_list = list(two_latest_draws)

        if not two_latest_draws_list:
          data = {'error': 'DrawResult data is empty'}
          return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

        winners_data = []
        for draw_id in two_latest_draws_list:
          winners = DrawResultWinner.objects.filter(drawResult=draw_id, isDeleted=False)
          serializer = DrawResultWinnerSerializer(winners, many=True)
          winners_data.append(serializer.data)

        return JsonResponse({'winners': winners_data}, status=status.HTTP_200_OK)