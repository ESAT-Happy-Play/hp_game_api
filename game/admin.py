from django.contrib import admin
from game.models import *
# Register your models here.

admin.site.register(CompanyGame)
admin.site.register(DrawResult)
admin.site.register(DrawResultWinner)
admin.site.register(Game)
admin.site.register(GameSchedule)
admin.site.register(GameDrawType)
admin.site.register(CloseDate)
admin.site.register(BetTransaction)