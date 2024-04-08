from game.serializers import BetItemSerializer, BetItemCreateSerializer, BetItemListPaginationSerializer
from game.models import BetItem
from .base_viewset import BaseViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import action
from django.http import JsonResponse
from rest_framework import status

class BetItemViewSet(BaseViewSet):
    queryset = BetItem.objects.filter(isDeleted=False)
    serializer_class = BetItemSerializer

    
    @extend_schema(request=BetItemCreateSerializer)
    def create(self, request):
        return super().create(request)
    
    
    @extend_schema(parameters=[
        OpenApiParameter(name='idList', description='add one or more id/s (commaseparated)', type=str),
        OpenApiParameter(name='accountId', description='add accountId', type=str),
        OpenApiParameter(name='companyGame', description='filter by companyGame', type=str),
    ])
    @action(detail=False, methods=["get"], url_path="list")
    def get_list(self, request, pk=None):
        filters= {}
        if 'idList' in request.query_params:
            filters['orderItemId__in'] = request.query_params.get('idList').split(',')
            
        if 'accountId' in request.query_params:
            filters['betTransaction__accountId'] = request.query_params.get('accountId')
            
        if 'companyGame' in request.query_params:
            filters['companyGame'] = request.query_params.get('companyGame')
            
        instance = self.queryset.select_related('betTransaction').filter(**filters)
        serializer = self.serializer_class(instance, many=True)

        return JsonResponse(data=serializer.data, status=status.HTTP_200_OK, safe=False)

    @extend_schema(request=BetItemListPaginationSerializer)
    @action(detail=False, methods=['post'], url_path='paginated-list')
    def get_paginated_bet_item_list(self, request):
        company_id = request.data.get('companyId', None)
        start_date = request.data.get('start_date', None)
        end_date = request.data.get('end_date', None)
        start = request.data.get('start', 0)
        size = request.data.get('size', 20)

        bet_items = self.queryset

        if company_id:
            bet_items = bet_items.filter(companyGame__companyId=company_id)

        if start_date:
            bet_items = bet_items.filter(betTransaction__dateOfTransaction__gte=start_date)

        if end_date:
            bet_items = bet_items.filter(betTransaction__dateOfTransaction__lte=end_date)

        bet_items = bet_items.order_by('-betTransaction__dateOfTransaction')  # order by date in descending order

        total = bet_items.count()
        data = bet_items[start:start + size]

        response_data = [
            {
                'id': item.id,
                'value': item.value,
                'orderItemId': item.orderItemId,
                'amount': item.amount,
                'dateOfTransaction': item.betTransaction.dateOfTransaction,
                'accountId': item.betTransaction.accountId,
                'transactionNumber': item.betTransaction.transactionNumber,
                'drawDate': item.gameSchedule.date,
                'drawTime': item.gameSchedule.drawTime
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