from game.serializers import CloseDateSerializer, CloseDateCreateSerializer, CloseDateUpdateSerializer
from game.models import CloseDate
from .base_viewset import BaseViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.http import JsonResponse
from rest_framework import status
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.db.models import Q
from rest_framework.decorators import action

class CloseDateViewSet(BaseViewSet):
    queryset = CloseDate.objects.filter(isDeleted=False)
    serializer_class = CloseDateSerializer

    @extend_schema(parameters=[
        OpenApiParameter(name='includeIsDeleted', description='isDeleted filter', type=bool),
        OpenApiParameter(name='status', description='status filter', type=int),
        OpenApiParameter(name='startDate', description='start date for date range filter: YYYY-MM-DD', type=str),
        OpenApiParameter(name='endDate', description='end date for date range filter: YYYY-MM-DD', type=str),
    ])
    @action(detail=False, methods=['get'], url_path='(?P<companyId>[^/.]+)/(?P<gameId>[^/.]+)')
    def closed_date_list(self, request, companyId=None, gameId=None):
        include_is_deleted = request.query_params.get('includeIsDeleted', 'true').lower() == 'true'
        status_filter = self.request.query_params.get('status', None)
        start_date_str = request.query_params.get('startDate', None)
        end_date_str = request.query_params.get('endDate', None)

        queryset = self.queryset.filter(companyId=companyId, game=gameId)

        if not include_is_deleted:
            queryset = self.queryset.filter(isDeleted=False)

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            queryset = queryset.filter(Q(date__gte=start_date))

        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            queryset = queryset.filter(Q(date__lte=end_date))

        serializer = self.serializer_class(queryset, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

    @extend_schema(request=CloseDateCreateSerializer)
    def create(self, request):
        return super().create(request)

    @extend_schema(request=CloseDateUpdateSerializer)
    def update(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = CloseDateUpdateSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)