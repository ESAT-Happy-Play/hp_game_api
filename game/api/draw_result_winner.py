from game.serializers import DrawResultWinnerSerializer, DrawResultWinnerCreateSerializer
from game.models import DrawResultWinner
from .base_viewset import BaseViewSet
from drf_spectacular.utils import extend_schema

class DrawResultWinnerViewSet(BaseViewSet):
    queryset = DrawResultWinner.objects.filter(isDeleted=False)
    serializer_class = DrawResultWinnerSerializer

    @extend_schema(request=DrawResultWinnerCreateSerializer)
    def create(self, request):
        return super().create(request)