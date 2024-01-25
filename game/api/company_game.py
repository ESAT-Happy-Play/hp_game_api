from game.serializers import CompanyGameSerializer
from game.models import CompanyGame
from .base_viewset import BaseViewSet
from rest_framework import viewsets, status
from django.http import JsonResponse

class CompanyGameViewSet(BaseViewSet):
    queryset = CompanyGame.objects.filter(isDeleted=False)
    serializer_class = CompanyGameSerializer


    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)