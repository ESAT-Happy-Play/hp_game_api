from game.serializers import PrizePoolSerializer
from game.models import PrizePool
from .base_viewset import BaseViewSet

class PrizePoolViewSet(BaseViewSet):
    queryset = PrizePool.objects.filter(isDeleted=False)
    serializer_class = PrizePoolSerializer
