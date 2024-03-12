from game.serializers import CompanyGameSerializer, GameScheduleSerializer, CompanyGameCreateSerializer, CompanyGameUpdateSerializer
from game.models import CompanyGame, GameSchedule
from .base_viewset import BaseViewSet
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from drf_spectacular.utils import extend_schema, OpenApiParameter
import uuid

class CompanyGameViewSet(BaseViewSet):
    queryset = CompanyGame.objects.filter(isDeleted=False)
    serializer_class = CompanyGameSerializer

    @extend_schema(parameters=[OpenApiParameter(name='companyId', description='companyId filter', type=str)])
    def list(self, request):
        queryset = self.queryset
        company_id = self.request.query_params.get('companyId', None)
        
        if company_id:
            try:
                company_id = uuid.UUID(company_id)
                queryset = queryset.filter(companyId__exact=company_id)
            except ValueError:
                return JsonResponse({"error": "Invalid UUID format for companyId"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(queryset, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        
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

    @action(detail=True, methods=["get"], url_path="schedules")
    def get_company_game_schedules(self,request, pk=None):
        company_game = get_object_or_404(self.queryset, pk=pk)
        schedules = GameSchedule.objects.filter(companyGame=company_game, isDeleted=False)
        
        schedules_serializer = GameScheduleSerializer(schedules, many=True)
        return JsonResponse(schedules_serializer.data, status=status.HTTP_200_OK, safe=False)