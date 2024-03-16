from rest_framework import serializers


class WinningMultiplierSerializer(serializers.Serializer):
    minAmount = serializers.IntegerField()
    winPerBet = serializers.IntegerField()


class PoolingSerializer(serializers.Serializer):
    prizeFloor = serializers.IntegerField()
    prizeCeiling = serializers.IntegerField()
    incrementAmount = serializers.IntegerField()


class BetLimitsSerializer(serializers.Serializer):
    betEntryLimit = serializers.IntegerField()
    betAmountLimit = serializers.IntegerField()
    uniqueCombination = serializers.IntegerField()

    
class BetPriceSerializer(serializers.Serializer):
    isFixed = serializers.BooleanField()
    amount = serializers.IntegerField()
    

class PrizeCalculationSerializer(serializers.Serializer):
    winningMultiplier = WinningMultiplierSerializer(required=False)
    pooling = PoolingSerializer(required=False)
    enableQuasi = serializers.BooleanField()
    consecutiveWins = serializers.IntegerField(required=False)
    

class GameSettingsSerializer(serializers.Serializer):
    betLimits = BetLimitsSerializer()
    betPrice = BetPriceSerializer()
    prizeCalculation = PrizeCalculationSerializer()


class StoreLimitsSerializer(serializers.Serializer):
    maxUnitsPrice = serializers.IntegerField()
    maxUnits = serializers.IntegerField(required=False)
    maxFavorites = serializers.IntegerField()
    hotCombinationsRange = serializers.IntegerField()
    hotCombinationsRefreshUnits = serializers.IntegerField()
    
class DeckLimitsSerializer(serializers.Serializer):
    deckOpenTime = serializers.IntegerField()
    maxDeckUnits = serializers.IntegerField()

class StoreSettingsSerializer(serializers.Serializer):
    storeLimits = StoreLimitsSerializer()
    deckLimits = DeckLimitsSerializer(required=False)