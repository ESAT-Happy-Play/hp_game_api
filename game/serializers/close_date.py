from rest_framework import serializers
from game.models import CloseDate

class CloseDateSerializer(serializers.ModelSerializer):
	class Meta:
		model = CloseDate
		fields = '__all__'