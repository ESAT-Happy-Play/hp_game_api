from game.serializers import DrawResultWinnerSerializer, DrawResultWinnerCreateSerializer, DrawResultWinnerUpdateSerializer
from game.models import DrawResultWinner, DrawResult, CompanyGame, Game
from game.serializers.draw_result_winner import DrawResultWinnerPaginationSerializer
from .base_viewset import BaseViewSet
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from django.shortcuts import get_object_or_404

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

    @action(detail=False, methods=['get'], url_path='unprocessed-credit')
    def get_unprocessed_credit_winners(self, request):
        winners = self.queryset.filter(isCreditProcessed=False)
        serializer = self.serializer_class(winners, many=True)

        for winner in serializer.data:

            winner_id = winner['id']
            transaction_no = f'HPWIN{str(winner_id).zfill(11)}'  # sample data: HPWIN00000000001
            transaction_reference = f'TRNWIN{str(winner_id).zfill(10)}' # sample data: TRNWIN00000000001

            draw_result = DrawResult.objects.get(id=winner['drawResult'])
            game_name = draw_result.companyGame.game.name

            winner['transactionNo'] = transaction_no
            winner['transactionReference'] = transaction_reference
            winner['notes'] = f'{game_name} WIN' # sample data: Regular WIN

        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

    @extend_schema(request=DrawResultWinnerUpdateSerializer)
    @action(detail=True, methods=['patch'], url_path="update-credit-processed")
    def update_winners_credit_processed(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data)

    @extend_schema(request=DrawResultWinnerPaginationSerializer)
    @action(detail=False, methods=['post'], url_path='list')
    def get_paginated_draw_result_winner(self, request):
        companygameId = request.data.get('companyGameId', None)
        start_date = request.data.get('start_date', None)
        end_date = request.data.get('end_date', None)
        start = request.data.get('start', 0)
        size = request.data.get('size', 10)

        draw_results = self.queryset

        if companygameId:
            draw_results = draw_results.filter(drawResult__companyGame=companygameId)

        if start_date:
            draw_results = draw_results.filter(drawResult__gameSchedule__date__gte=start_date)

        if end_date:
            draw_results = draw_results.filter(drawResult__gameSchedule__date__lte=end_date)

        draw_results = draw_results.order_by('-drawResult__gameSchedule__date', '-drawResult__gameSchedule__drawTime')  # order by date in descending order, then by draw time in descending order

        total = draw_results.count()
        data = draw_results[start:start + size]

        response_data = [
            {
                'id': item.id,
                'result': item.drawResult.result,
                'amount': item.amount,
                'companyGame': item.drawResult.companyGame.id,
                'gameSchedule': item.drawResult.gameSchedule.id,
                'drawDate': item.drawResult.gameSchedule.date,
                'drawTime': item.drawResult.gameSchedule.drawTime,
                'accountId': item.accountInfoId,
                'drawResult': item.drawResult.id
            }
            for item in data
        ]

        response_body = {
            "count": start + size,
            "offset":  start + size if start + size < total else 0,
            "totalCount": total,
            "data": response_data
        }

        return JsonResponse(response_body, status=status.HTTP_200_OK)