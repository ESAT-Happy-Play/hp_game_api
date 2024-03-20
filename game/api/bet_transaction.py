from game.serializers import BetTransactionSerializer, BetTransactionCreateSerializer, BetItemCreateSerializer
from game.models import BetTransaction
from .base_viewset import BaseViewSet
from django.db.models import Max
from drf_spectacular.utils import extend_schema
from django.http import JsonResponse
from rest_framework import status

class BetTransactionViewSet(BaseViewSet):
    queryset = BetTransaction.objects.filter(isDeleted=False).prefetch_related('betItems').all()
    serializer_class = BetTransactionSerializer

    @extend_schema(request=BetTransactionCreateSerializer, responses=BetTransactionSerializer)
    def create(self, request):
        max_id = BetTransaction.objects.aggregate(Max('id'))['id__max'] # get the maximum existing id in the table
        next_id = max_id + 1 if max_id is not None else 1
        transaction_number = str(next_id).zfill(16) # generate transactionNumber
        request.data['transactionNumber'] = transaction_number
        request.data['numberOfBets'] = len(request.data["betItems"])
        serializer = BetTransactionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = self.serializer_class(BetTransaction.objects.filter(pk=next_id).prefetch_related('betItems').first()) #refactor if possible, only for return of object purposes

        return JsonResponse(data=response.data, status=status.HTTP_201_CREATED, safe=False)
