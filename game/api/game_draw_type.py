from game.serializers import GameDrawTypeSerializer, GameDrawTypeUpdateSerializer, GameDrawTypeCreateSerializer
from game.models import GameDrawType, GameSchedule
from .base_viewset import BaseViewSet
from rest_framework import status
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from datetime import datetime
from rest_framework.decorators import action

class GameDrawTypeViewSet(BaseViewSet):
    queryset = GameDrawType.objects.all()
    active_queryset = queryset.filter(isDeleted=False)
    serializer_class = GameDrawTypeSerializer

    @extend_schema(parameters=[
        OpenApiParameter(name='includeIsDeleted', description='isDeleted filter', type=bool),
        OpenApiParameter(name='gameId', description='Game ID', type=int, location=OpenApiParameter.PATH),
    ],
    operation_id='game_draw_type_list_with_path_params')
    @action(detail=False, methods=['get'], url_path='(?P<companyId>[^/.]+)/(?P<gameId>[^/.]+)')
    def game_draw_type_list(self, request, companyId=None, gameId=None):
        include_is_deleted = request.query_params.get('includeIsDeleted', 'true').lower() == 'true'
        queryset = self.queryset.filter(companyId=companyId, game=gameId)

        if not include_is_deleted:
            queryset = queryset.filter(isDeleted=False)

        serializer = self.serializer_class(queryset, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
    

    @extend_schema(request=GameDrawTypeCreateSerializer)
    def create(self, request):
        time = datetime.strptime(request.data['drawTime'], '%H:%M:%S')
        request.data['gameDrawTypeName'] = time.strftime('%I:%M %p').lstrip('0')
        return super().create(request)
    

    @extend_schema(request=GameDrawTypeUpdateSerializer)
    def update(self, request, pk=None):
        instance = get_object_or_404(self.active_queryset, pk=pk)
        serializer = GameDrawTypeUpdateSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if instance.id is not None:
            game_schedules = GameSchedule.objects.filter(
                gameDrawType = instance,
                status = 0  # schedules that are NOT yet drawn
            ).update(
                openSchedule = instance.openSchedule,
                endCutOff = instance.endCutOff
            )

        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
