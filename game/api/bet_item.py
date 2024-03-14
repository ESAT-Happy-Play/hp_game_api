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
        OpenApiParameter(name='id_list', description='add one or more id/s (commaseparated)', type=str)
    ])
    @action(detail=False, methods=["get"], url_path="list")
    def get_list(self, request, pk=None):
        id_list = request.query_params.get('id_list', 'true').split(',')
        instance = self.queryset.filter(orderItemId__in=id_list)
        serializer = self.serializer_class(instance, many=True)

        return JsonResponse(data=serializer.data, status=status.HTTP_200_OK, safe=False)