from game.serializers import WinStreakSerializer
from game.models import WinStreak
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

class WinStreakViewSet(generics.ListCreateAPIView,viewsets.ViewSet):
    queryset = WinStreak.objects.all()
    serializer_class = WinStreakSerializer


    @extend_schema(request=WinStreakSerializer(many=True))
    def create(self, request, *args, **kwargs):  
        serializer = self.get_serializer(data=request.data, many=True)  
        serializer.is_valid(raise_exception=True)  
    
        try:  
            self.perform_create(serializer)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)  
        except:  
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['delete'])
    def delete_all(self, request):
        self.queryset.delete()
        return Response(status=status.HTTP_200_OK)  
