from game.serializers import CloseDateSerializer
from game.models import CloseDate, GameDrawType
from .base_viewset import BaseViewSet
from rest_framework import viewsets, status
from django.http import JsonResponse

class CloseDateViewSet(BaseViewSet):
    queryset = CloseDate.objects.filter(isDeleted=False)
    serializer_class = CloseDateSerializer

    def create(self, request):
        # validate closedDrawTypes
        closed_draw_types = request.data.get('closedDrawTypes', [])
        valid_ids = GameDrawType.objects.filter(isDeleted=False, id__in=closed_draw_types).values_list('id', flat=True)
        invalid_ids = set(closed_draw_types) - set(valid_ids)

        if invalid_ids:
            return JsonResponse(
                {'error': f"Invalid GameDrawType IDs: {', '.join(map(str, invalid_ids))}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
