from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter

class BaseViewSet(viewsets.ViewSet):
    """Allows basic operations like list, retrieve, delete, """
    """ when using this provide:        """
    """ - queryset                      """
    """ - serializer_class              """
    queryset = ()
    serializer_class = ()
    # To implement: JWT auth from the core identity service
    permission_classes = [IsAuthenticated]


    @extend_schema(parameters=[OpenApiParameter(name='includeIsDeleted', description='isDeleted filter', type=bool)])
    def list(self, request):
        include_is_deleted = request.query_params.get('includeIsDeleted', 'true').lower() == 'true'
        queryset = self.queryset

        if not include_is_deleted:
            queryset = self.queryset.filter(isDeleted=False)

        serializer = self.serializer_class(queryset, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
    
    def retrieve(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(instance)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def delete(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        instance.isDeleted = True
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data)
