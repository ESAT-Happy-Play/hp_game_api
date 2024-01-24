from game.serializers import DrawResultSerializer
from game.models import DrawResult
from .base_viewset import BaseViewSet

class DrawResultViewSet(BaseViewSet):
    queryset = DrawResult.objects.filter(isDeleted=False)
    serializer_class = DrawResultSerializer()
