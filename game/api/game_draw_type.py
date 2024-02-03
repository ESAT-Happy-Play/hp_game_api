from game.serializers import GameDrawTypeSerializer, GameDrawTypeCreateSerializer
from game.models import GameDrawType
from .base_viewset import BaseViewSet
from drf_spectacular.utils import extend_schema
from datetime import datetime

class GameDrawTypeViewSet(BaseViewSet):
    queryset = GameDrawType.objects.filter(isDeleted=False)
    serializer_class = GameDrawTypeSerializer

    @extend_schema(request=GameDrawTypeCreateSerializer)
    def create(self, request):
        print(type(request.data['drawTime']), request.data['drawTime'])
        time = datetime.strptime(request.data['drawTime'], '%H:%M:%S')
        request.data['gameDrawTypeName'] = time.strftime('%I:%M %p').lstrip('0')
        return super().create(request)