from rest_framework import serializers
from active_code.models import ActiveCodeModel


class ActiveCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveCodeModel
        fields = '__all__'
