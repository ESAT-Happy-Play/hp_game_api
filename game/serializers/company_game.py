from rest_framework import serializers
from game.models import CompanyGame

class CompanyGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyGame
        fields = '__all__'