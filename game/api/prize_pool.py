from game.serializers import PrizePoolSerializer, PrizePoolCreateSerializer
from game.models import PrizePool
from .base_viewset import BaseViewSet
from drf_spectacular.utils import extend_schema

class PrizePoolViewSet(BaseViewSet):
    queryset = PrizePool.objects.filter(isDeleted=False)
    serializer_class = PrizePoolSerializer

    @extend_schema(request=PrizePoolCreateSerializer)
    def create(self, request):
        return super().create(request)