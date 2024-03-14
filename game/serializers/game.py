from rest_framework import serializers
from game.models import Game

class GameSerializer(serializers.ModelSerializer):
    class Meta:
      model = Game
      fields = '__all__'

    def validate(self, data):
        game_mechanics = data.get('gameMechanics', {})
        n_cards = game_mechanics.get('nCards')
        n_suites = game_mechanics.get('nSuites')

        if n_cards is None:
            raise serializers.ValidationError("nCards attribute in gameMechanics is required")
        if n_suites is None and 'nSuites' not in game_mechanics:
            raise serializers.ValidationError("nSuites attribute in gameMechanics is required")

        return data

class GameCreateSerializer(GameSerializer):
    class Meta:
        model = Game
        exclude = ('isDeleted',)