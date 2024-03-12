from game.serializers import CombinationLimitSerializer
from game.models import CombinationLimit
from .base_viewset import BaseViewSet
from drf_spectacular.utils import extend_schema
from django.http import JsonResponse
from rest_framework import status
from django.shortcuts import get_object_or_404

class CombinationLimitViewSet(BaseViewSet):
    queryset = CombinationLimit.objects.all()
    serializer_class = CombinationLimitSerializer

    @extend_schema(request=CombinationLimitSerializer)
    def update(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = CombinationLimitSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
