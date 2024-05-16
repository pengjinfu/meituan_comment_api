from rest_framework import serializers
from mt_order.models import MTOrderModel


class MTOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MTOrderModel
        fields = '__all__'
