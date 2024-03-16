from django.db import models
from game.models.game import Game

class CompanyGame(models.Model):
    """Model definition for CompanyGame.
    gameSettings structure:
        "betLimits":{
            "betEntryLimit": int,
            "betAmountLimit": int,
            "uniqueCombination": int
        },
        "betPrice": {
            "isFixed": bool,
            "amount": int (if fixed, this is betPrice, else this is betPriceLimit)
        },
        "prizeCalculation":{
            "winningMultiplier" : {
                "winPerBet": int,
                "minAmount": int,
            },
            "pooling" : {
                "prizeFloor": int,
                "prizeCeiling": int,
                "incrementAmount":int
            },
            "enableQuasi": bool ,
            "consecutiveWins":int
        }

    storeLimits structure:
    
        "storeLimits":{
            "maxUnitsPrice": int,
            "maxUnitsRegular": int,
            "maxUnitsPowerWin": int,
            "maxFavorites": int,
            "hotCombinationsRange": int,
            "hotCombinationsRefreshUnits": int
        },
        "deckLimits": {
            "deckOpenTime": int(in mins),
            "maxDeckUnits": int
        }
    """
    def game_settings_default():
        return{
            "betLimits": {
                "betEntryLimit": 5,
                "betAmountLimit": 10000,
                "uniqueCombination": 70
            },
            "betPrice": {
                "isFixed": True,
                "amount": 10
            },
            "prizeCalculation":{
                "pooling" : {
                    "prizeFloor": 10000,
                    "prizeCeiling": 15000000,
                    "incrementAmount":10
                },
                "enableQuasi": True
            }
        }
    
    def store_settings_default():
        return {
            "storeLimits":{
                "maxUnitsPrice": 1000,
                "maxUnits": 20,
                "maxFavorites": 20,
                "hotCombinationsRange": 10,
                "hotCombinationsRefreshUnits": 20
                },
            "deckLimits": {
                "deckOpenTime": 5,
                "maxDeckUnits": 25
            }
        }
    
    companyId = models.UUIDField()
    game = models.ForeignKey(Game, verbose_name=("Game"), on_delete=models.CASCADE)
    gameSettings = models.JSONField("GameSettings", default=game_settings_default)
    storeSettings = models.JSONField("StoreSettings", default=store_settings_default)
    livestream = models.URLField(null=True)
    isDeleted= models.BooleanField(default=False)

    def __str__(self):
        """Unicode representation of CompanyGame."""
        return "<Company Game Id: {self.id}>"

