from game.serializers import BaseCompanyGameSerializer, GameScheduleSerializer, CompanyGameCreateSerializer, CompanyGameUpdateSerializer, BetLimitsSerializer, PrizeCalculationSerializer, BetPriceSerializer, StoreLimitsSerializer, DeckLimitsSerializer, CompanyGameListSerializer
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
    serializer_class = BaseCompanyGameSerializer

    @extend_schema(parameters=[OpenApiParameter(name='companyId', description='companyId filter', type=str)],
                   responses=CompanyGameListSerializer)
    def list(self, request):
        queryset = self.queryset
        company_id = self.request.query_params.get('companyId', None)
        if company_id:
            try:
                company_id = uuid.UUID(company_id)
                queryset = queryset.filter(companyId__exact=company_id)
            except ValueError:
                return JsonResponse({"error": "Invalid UUID format for companyId"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CompanyGameListSerializer(queryset, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        

    @extend_schema(request=CompanyGameCreateSerializer, responses=CompanyGameCreateSerializer)
    def create(self, request):
        serializer = CompanyGameCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)


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
    def get_draw_current(self, request, pk=None):
        company_game = get_object_or_404(self.queryset, pk=pk)
        current_time = datetime.now().time()
        current_date = datetime.now().date()
        types = GameSchedule.objects.filter(date=current_date, companyGame=company_game, gameDrawType__drawTime__lte=current_time, gameDrawType__drawTime__gte=(datetime.now()-timedelta(minutes=5))).first()
        if types == None:
            return JsonResponse({"details": "No open current schedule yet"}, status=status.HTTP_404_NOT_FOUND)
        
        type_serializer = GameScheduleSerializer(types)
        return JsonResponse(type_serializer.data, status=status.HTTP_200_OK)
    

    @action(detail=True, methods=["get"], url_path="draw/next")
    def get_draw_next(self, request, pk=None):
        company_game = get_object_or_404(self.queryset, pk=pk)
        current_time = datetime.now().time()
        current_date = datetime.now().date()
        types = GameSchedule.objects.filter(date=current_date, companyGame=company_game, gameDrawType__drawTime__gte=current_time).first()
        if types == None:
            return JsonResponse({"details": "No open next schedule for today yet"}, status=status.HTTP_404_NOT_FOUND)
        
        type_serializer = GameScheduleSerializer(types)
        return JsonResponse(type_serializer.data, status=status.HTTP_200_OK)


    @action(detail=True, methods=["get"], url_path="draw/backlogs")
    def get_draw_backlogs(self, request, pk=None):
        company_game = get_object_or_404(self.queryset, pk=pk)
        current_date = datetime.now().date()
        backlogs = GameSchedule.objects.filter(companyGame=company_game, status=0, date__lte=current_date, gameDrawType__drawTime__lte=(datetime.now()-timedelta(minutes=5)), isDeleted=False)
        backlogs_serializer = GameScheduleSerializer(backlogs, many=True)
        return JsonResponse(backlogs_serializer.data, status=status.HTTP_200_OK, safe=False)


    @action(detail=True, methods=["get"], url_path="schedules")
    def get_company_game_schedules(self, request, pk=None):
        company_game = get_object_or_404(self.queryset, pk=pk)
        schedules = GameSchedule.objects.filter(companyGame=company_game, isDeleted=False)
        schedules_serializer = GameScheduleSerializer(schedules, many=True)
        return JsonResponse(schedules_serializer.data, status=status.HTTP_200_OK, safe=False)
    

    # Chunk Endpoints

    @extend_schema(request=BetPriceSerializer, responses=BetPriceSerializer)
    @action(detail=True, methods=["get", "patch"], url_path="bet-price")
    def chunk_bet_price(self, request, pk=None):
        if(request.method == 'GET'):
            company_game = get_object_or_404(self.queryset, pk=pk)
            bet_price = company_game.gameSettings["betPrice"]
            return JsonResponse(bet_price, status=status.HTTP_200_OK)
        
        if(request.method == 'PATCH'):
            instance = get_object_or_404(self.queryset, pk=pk)
            bet_price = BetPriceSerializer(data=request.data)
            bet_price.is_valid(raise_exception=True)

            instance.gameSettings["betPrice"] = request.data
            serializer = self.serializer_class(instance, data=instance.gameSettings["betPrice"], partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse(serializer.data.get("gameSettings")["betPrice"])
        
    
    @extend_schema(request=PrizeCalculationSerializer, responses=PrizeCalculationSerializer)
    @action(detail=True, methods=["get", "patch"], url_path="prize-calculation")
    def chunk_prize_calculation(self, request, pk=None):
        if(request.method == 'GET'):
            company_game = get_object_or_404(self.queryset, pk=pk)
            prize_calculation = company_game.gameSettings["prizeCalculation"]
            return JsonResponse(prize_calculation, status=status.HTTP_200_OK)
        
        if(request.method == 'PATCH'):
            instance = get_object_or_404(self.queryset, pk=pk)
            prize_calculation = PrizeCalculationSerializer(data=request.data)
            prize_calculation.is_valid(raise_exception=True)

            instance.gameSettings["prizeCalculation"] = request.data
            serializer = self.serializer_class(instance, data=instance.gameSettings["prizeCalculation"], partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse(serializer.data.get("gameSettings")["prizeCalculation"])
    
    
    @extend_schema(request=BetLimitsSerializer, responses=BetLimitsSerializer)
    @action(detail=True, methods=["get", "patch"], url_path="bet-limits")
    def chunk_bet_limits(self, request, pk=None):
        if(request.method == 'GET'):
            company_game = get_object_or_404(self.queryset, pk=pk)
            bet_limits = company_game.gameSettings["betLimits"]
            return JsonResponse(bet_limits, status=status.HTTP_200_OK)
        
        if(request.method == 'PATCH'):
            instance = get_object_or_404(self.queryset, pk=pk)
            betLimitsSerializer = BetLimitsSerializer(data=request.data)
            betLimitsSerializer.is_valid(raise_exception=True)
            
            instance.gameSettings["betLimits"] = request.data
            serializer = self.serializer_class(instance, data=instance.gameSettings["betLimits"], partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse(serializer.data.get("gameSettings")["betLimits"])
        
        
    @extend_schema(request=StoreLimitsSerializer, responses=StoreLimitsSerializer)
    @action(detail=True, methods=["get", "patch"], url_path="store-limits")
    def chunk_store_limits(self, request, pk=None):
        if(request.method == 'GET'):
            company_game = get_object_or_404(self.queryset, pk=pk)
            store_limits = company_game.storeSettings["storeLimits"]
            return JsonResponse(store_limits, status=status.HTTP_200_OK)
        
        if(request.method == 'PATCH'):
            instance = get_object_or_404(self.queryset, pk=pk)
            storeLimitsSerializer = StoreLimitsSerializer(data=request.data)
            storeLimitsSerializer.is_valid(raise_exception=True)   

            instance.storeSettings["storeLimits"] = request.data
            serializer = self.serializer_class(instance, data=instance.storeSettings["storeLimits"], partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse(serializer.data.get("storeSettings")["storeLimits"])
        
    
    
    @extend_schema(request=DeckLimitsSerializer, responses=DeckLimitsSerializer)
    @action(detail=True, methods=["get", "patch"], url_path="deck-limits")
    def chunk_deck_limits(self, request, pk=None):
        if(request.method == 'GET'):
            company_game = get_object_or_404(self.queryset, pk=pk)
            deck_limits = company_game.storeSettings["deckLimits"]
            return JsonResponse(deck_limits, status=status.HTTP_200_OK)
        
        if(request.method == 'PATCH'):
            instance = get_object_or_404(self.queryset, pk=pk)
            deckLimitsSerializer = DeckLimitsSerializer(data=request.data)
            deckLimitsSerializer.is_valid(raise_exception=True)   

            instance.storeSettings["deckLimits"] = request.data
            serializer = self.serializer_class(instance, data=instance.storeSettings["deckLimits"], partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse(serializer.data.get("storeSettings")["deckLimits"])
    
    