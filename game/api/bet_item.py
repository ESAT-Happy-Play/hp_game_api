from game.serializers import BetItemSerializer
from game.models import BetItem
from .base_viewset import BaseViewSet

class BetItemViewSet(BaseViewSet):
    queryset = BetItem.objects.filter(isDeleted=False)
    serializer_class = BetItemSerializer