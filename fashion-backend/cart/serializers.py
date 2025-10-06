from rest_framework import serializers
from . import models 
from core.serializers import ProductSerializer

class CartSerializer(serializers.Serializer):
    product = ProductSerializer
    class Meta:
        model = models.Cart
        exclude = ['userid','created_at','updated_at']