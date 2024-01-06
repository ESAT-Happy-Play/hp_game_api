from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from game.serializers import CompanyGameSerializer
from rest_framework import viewsets
from game.models import CompanyGame

class CompanyGameViewSet(viewsets.ViewSet):
    queryset = CompanyGame.objects.all()

    def list(self, request):
        serializer = CompanyGameSerializer(self.queryset, many=True)
        return JsonResponse(serializer.data)
    
    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = CompanyGameSerializer(user)
        return JsonResponse(serializer.data)