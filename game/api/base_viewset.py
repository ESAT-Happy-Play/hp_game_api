from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

class BaseViewSet(viewsets.ViewSet):
    """Allows basic operations like list, retrieve, delete, """
    """ when using this provide:        """
    """ - queryset                      """
    """ - serializer_class              """
    queryset = ()
    serializer_class = ()
    # To implement: JWT auth from the core identity service
    # permission_classes = [IsAuthenticated]

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
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

    @action(detail=True, methods=['put'])
    def delete(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        instance.isDeleted = True
        serializer = self.serializer_class(instance)
        serializer.save()
        return JsonResponse(serializer.data)
    

