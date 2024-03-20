from game.serializers import BetItemSerializer, BetItemCreateSerializer
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