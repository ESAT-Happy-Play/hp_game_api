from game.serializers import BetItemSerializer, BetItemCreateSerializer
from game.models import BetItem
from .base_viewset import BaseViewSet
from drf_spectacular.utils import extend_schema

class BetItemViewSet(BaseViewSet):
    queryset = BetItem.objects.filter(isDeleted=False)
    serializer_class = BetItemSerializer

    
    @extend_schema(request=BetItemCreateSerializer)
    def create(self, request):
        return super().create(request)