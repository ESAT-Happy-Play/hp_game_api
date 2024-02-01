from game.serializers import DrawResultSerializer
from game.models import DrawResult
from .base_viewset import BaseViewSet
from django.http import JsonResponse
from rest_framework import status
import requests
from dotenv import load_dotenv
import os

load_dotenv(override=True)

class DrawResultViewSet(BaseViewSet):
    queryset = DrawResult.objects.filter(isDeleted=False)
    serializer_class = DrawResultSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        #broadcasting winners
        requests.post(url=os.environ.get("SOCKET_SERVICE_URL")+"draw-result", data=request.data['result'])


        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)