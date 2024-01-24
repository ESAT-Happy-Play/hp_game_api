from game.serializers import DrawResultWinnerSerializer
from game.models import DrawResultWinner
from .base_viewset import BaseViewSet

class DrawResultWinnerViewSet(BaseViewSet):
    queryset = DrawResultWinner.objects.filter(isDeleted=False)
    serializer_class = DrawResultWinnerSerializer()
