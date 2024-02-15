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
        two_latest_draws = DrawResult.objects.all().order_by('-id')[:2].values_list('id', flat=True)
        two_latest_draws_list = list(two_latest_draws)

        if len(two_latest_draws_list) != 2:
          data = {'error': 'DrawResult objects are fewer than 2'}
          return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)

        winners1 = DrawResultWinner.objects.filter(drawResult=two_latest_draws_list[0], isDeleted=False)
        winners2 = DrawResultWinner.objects.filter(drawResult=two_latest_draws_list[1], isDeleted=False)
        serializer1 = DrawResultWinnerSerializer(winners1, many=True)
        serializer2 = DrawResultWinnerSerializer(winners2, many=True)

        data = {
          '1st_latest_draw_winners': serializer1.data,
          '2nd_latest_draw_winners': serializer2.data
        }
        return JsonResponse(data, status=status.HTTP_200_OK)