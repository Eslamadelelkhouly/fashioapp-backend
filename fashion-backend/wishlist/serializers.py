from rest_framework import serializers
from . import models

class WishListSerializers(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='product.id')
    title = serializers.ReadOnlyField(source='product.title')
    description = serializers.ReadOnlyField(source='product.description')
    is_featured = serializers.ReadOnlyField(source='product.is_featured')
    clothesType = serializers.ReadOnlyField(source='product.clothesType')
    ratings = serializers.ReadOnlyField(source='product.ratings')
    category = serializers.ReadOnlyField(source='product.category')
    brand = serializers.ReadOnlyField(source='product.brand')
    sizes = serializers.ReadOnlyField(source='product.sizes')
    colors = serializers.ReadOnlyField(source='product.colors')
    imageUrl = serializers.ReadOnlyField(source='product.imageUrl')
    created_at = serializers.RelatedField(source='product.created_at')

    class Meta:
        model = models.WishList
        fields = ['id','title','description' , 'is_featured','clothesType', 'ratings' , 'category' , 'brand','sizes' ,'colors','imageUrl' , 'created_at']