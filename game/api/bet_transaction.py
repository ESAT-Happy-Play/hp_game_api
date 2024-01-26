from game.serializers import BetTransactionSerializer
from game.models import BetTransaction
from .base_viewset import BaseViewSet
from django.db.models import Max

class BetTransactionViewSet(BaseViewSet):
    queryset = BetTransaction.objects.filter(isDeleted=False)
    serializer_class = BetTransactionSerializer

    def create(self, request):
        max_id = BetTransaction.objects.aggregate(Max('id'))['id__max'] # get the maximum existing id in the table
        next_id = max_id + 1 if max_id is not None else 1
        transaction_number = str(next_id).zfill(16) # generate transactionNumber
        request.data['transactionNumber'] = transaction_number
        return super().create(request) # still uses BaseViewSet create after parsing transactionNumber
