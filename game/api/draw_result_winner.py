from game.serializers import DrawResultWinnerSerializer, DrawResultWinnerCreateSerializer
from game.models import DrawResultWinner, DrawResult
from .base_viewset import BaseViewSet
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status

class DrawResultWinnerViewSet(BaseViewSet):
    queryset = DrawResultWinner.objects.filter(isDeleted=False)
    serializer_class = DrawResultWinnerSerializer

    @extend_schema(request=DrawResultWinnerCreateSerializer)
    def create(self, request):
        return super().create(request)
    
    @extend_schema(parameters=[
        OpenApiParameter(name='accountId', description='Account Id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    operation_id='account_latest_draw_result_winner')
    @action(detail=False, methods=['get'], url_path='(?P<accountId>[^/.]+)/account-latest')
    def account_latest_draw_result_winner(self, request, accountId=None):
        draw_result = self.queryset.filter(accountInfoId__exact=accountId).last()

        if draw_result is None:
            return JsonResponse({'detail': 'No winning records for this account'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(draw_result)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    