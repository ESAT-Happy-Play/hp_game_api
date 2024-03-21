from game.serializers import BetTransactionSerializer, BetTransactionCreateSerializer, BetItemSerializer, BetTransactionPageListSerializer, TransactionPaginationSerializer
from game.models import BetTransaction, BetItem
from .base_viewset import BaseViewSet
from django.db.models import Max
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

class BetTransactionViewSet(BaseViewSet):
    queryset = BetTransaction.objects.filter(isDeleted=False).prefetch_related('betItems').all()
    serializer_class = BetTransactionSerializer

    @extend_schema(request=BetTransactionCreateSerializer, responses=BetTransactionSerializer)
    def create(self, request):
        max_id = BetTransaction.objects.aggregate(Max('id'))['id__max'] # get the maximum existing id in the table
        next_id = max_id + 1 if max_id is not None else 1
        request.data['numberOfBets'] = len(request.data["betItems"])
        serializer = BetTransactionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = self.serializer_class(BetTransaction.objects.filter(pk=next_id).prefetch_related('betItems').first()) #refactor if possible, only for return of object purposes

        return JsonResponse(data=response.data, status=status.HTTP_201_CREATED, safe=False)
    
    
    @action(detail=True, methods=["get"], url_path="bet-items")
    def get_betitems_by_transaction(self, request, pk=None):
        bet_transaction = get_object_or_404(self.queryset, pk=pk)
        schedules = BetItem.objects.filter(betTransaction=bet_transaction, isDeleted=False)
        schedules_serializer = BetItemSerializer(schedules, many=True)
        return JsonResponse(schedules_serializer.data, status=status.HTTP_200_OK, safe=False)
    

    @extend_schema(request=TransactionPaginationSerializer, responses=TransactionPaginationSerializer)
    @action(detail=False, methods=['post'], url_path='list')
    def paginated_list(self,request):
        size = request.data.pop('size')
        start = request.data.pop('start')
        queryset = self.queryset
        total = queryset.count()
        data = queryset[start:start+size]
        serializer = BetTransactionPageListSerializer(data, many=True)
        # print(serializer.data)
        paginated_data = {"start":start+size, "total":total, "data":[]}
        paginated_data['data']=serializer.data
        return Response(data=paginated_data, status=status.HTTP_200_OK)
