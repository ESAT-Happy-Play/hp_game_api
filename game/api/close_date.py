from game.serializers import CloseDateSerializer, CloseDateCreateSerializer
from game.models import CloseDate
from .base_viewset import BaseViewSet
from drf_spectacular.utils import extend_schema

class CloseDateViewSet(BaseViewSet):
    queryset = CloseDate.objects.filter(isDeleted=False)
    serializer_class = CloseDateSerializer

    @extend_schema(request=CloseDateCreateSerializer)
    def create(self, request):
        return super().create(request)