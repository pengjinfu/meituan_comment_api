from rest_framework import serializers
from mall.models import MallModel


class MallSerializer(serializers.ModelSerializer):
    class Meta:
        model = MallModel
        fields = '__all__'
