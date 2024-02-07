from game.serializers import CompanyGameSerializer, GameScheduleSerializer, CompanyGameCreateSerializer, CompanyGameUpdateSerializer
from game.models import CompanyGame, GameSchedule
from .base_viewset import BaseViewSet
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from drf_spectacular.utils import extend_schema

class CompanyGameViewSet(BaseViewSet):
    queryset = CompanyGame.objects.filter(isDeleted=False)
    serializer_class = CompanyGameSerializer

    
    @extend_schema(request=CompanyGameCreateSerializer)
    def create(self, request):
        return super().create(request)

    @extend_schema(request=CompanyGameUpdateSerializer)
    def update(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = CompanyGameUpdateSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="bets/current")
    def get_bet_current(self,request, pk=None):
        company_game = get_object_or_404(self.queryset, pk=pk)
        current_time = datetime.now().time()
        current_date = datetime.now().date()
        types = GameSchedule.objects.filter(date=current_date, companyGame=company_game, gameDrawType__openSchedule__lte=current_time, gameDrawType__endCutOff__gte=current_time).first()
        if types == None:
            return JsonResponse({"details": "No open bet schedule yet"}, status=status.HTTP_404_NOT_FOUND)
        
        type_serializer = GameScheduleSerializer(types)
        return JsonResponse(type_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="draw/current")
    def get_draw_current(self,request, pk=None):
        company_game = get_object_or_404(self.queryset, pk=pk)
        current_time = datetime.now().time()
        current_date = datetime.now().date()
        types = GameSchedule.objects.filter(date=current_date, companyGame=company_game, gameDrawType__drawTime__lte=current_time, gameDrawType__drawTime__gte=(datetime.now()-timedelta(minutes=5))).first()
        if types == None:
            return JsonResponse({"details": "No open current schedule yet"}, status=status.HTTP_404_NOT_FOUND)
        
        type_serializer = GameScheduleSerializer(types)
        return JsonResponse(type_serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["get"], url_path="draw/next")
    def get_draw_next(self,request, pk=None):
        company_game = get_object_or_404(self.queryset, pk=pk)
        current_time = datetime.now().time()
        current_date = datetime.now().date()
        types = GameSchedule.objects.filter(date=current_date, companyGame=company_game, gameDrawType__drawTime__gte=current_time).first()
        if types == None:
            return JsonResponse({"details": "No open next schedule for today yet"}, status=status.HTTP_404_NOT_FOUND)
        
        type_serializer = GameScheduleSerializer(types)
        return JsonResponse(type_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="draw/backlogs")
    def get_draw_backlogs(self,request, pk=None):
        company_game = get_object_or_404(self.queryset, pk=pk)
        current_date = datetime.now().date()
        backlogs = GameSchedule.objects.filter(companyGame=company_game, status=0, date__lte=current_date, gameDrawType__drawTime__lte=(datetime.now()-timedelta(minutes=5)), isDeleted=False)
        
        backlogs_serializer = GameScheduleSerializer(backlogs, many=True)
        return JsonResponse(backlogs_serializer.data, status=status.HTTP_200_OK, safe=False)