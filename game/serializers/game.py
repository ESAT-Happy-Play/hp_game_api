from rest_framework import serializers
from game.models import Game

class GameSerializer(serializers.ModelSerializer):
    class Meta:
      model = Game
      fields = '__all__'

    def validate(self, data):
        game_mechanics = data.get('gameMechanics', {})
        n_cards = game_mechanics.get('n_cards')
        n_suites = game_mechanics.get('n_suites')

        if n_cards is None:
            raise serializers.ValidationError("n_cards field is required")
        if n_suites is None and 'n_suites' not in game_mechanics:
            raise serializers.ValidationError("n_suites field is required")

        return data

class GameCreateSerializer(GameSerializer):
    class Meta:
        model = Game
        exclude = ('isDeleted',)