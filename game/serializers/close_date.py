from rest_framework import serializers
from game.models import CloseDate

class CloseDateSerializer(serializers.ModelSerializer):
	class Meta:
		model = CloseDate
		fields = '__all__'

class CloseDateCreateSerializer(CloseDateSerializer):
    class Meta:
        model = CloseDate
        exclude = ('isDeleted',)

class CloseDateUpdateSerializer(CloseDateSerializer):
    class Meta:
        model = CloseDate
        fields = ('status', 'game')