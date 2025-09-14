from django.shortcuts import render
import random
from rest_framework import generics , status
from rest_framework.views import APIView
from . import models , serializers
from django.db.models import Count
from rest_framework.response import Response
# Create your views here.

class CategoryList(generics.ListAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()

class HomeCategoryList(generics.ListAPIView):
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        queryset = models.Category.objects.all()
        queryset = queryset.annotate(random_order=Count('id'))
        queryset = list(queryset)
        random.shuffle(queryset)
        return queryset[:5]


class BrandList(generics.ListAPIView):
    serializer_class = serializers.BrandSerializer
    queryset = models.Brand.objects.all()

class ProductList(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        queryset = models.Product.objects.all()
        queryset = queryset.annotate(random_order=Count('id'))
        queryset = list(queryset)
        random.shuffle(queryset)
        return queryset[:20]

class PopularProductList(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        queryset = models.Product.objects.filter(rating_gte=4.0 , rating_lte=5.0)
        queryset = queryset.annotate(random_order=Count('id'))
        queryset = list(queryset)
        random.shuffle(queryset)
        return queryset[:20]


class ProductListByClothesType(APIView):
    serializer_class = serializers.ProductSerializer

    def get(self , request):
        query = request.query_params.get('clothesType' , None)
        if query:
            queryset = models.Product.objects.filter(clothesType=query)
            queryset = queryset.annotate(random_order=Count('id'))
            product_list = list(queryset)
            random.shuffle(product_list)
            limited_products = product_list[:20]

            serializer = serializers.ProductSerializer(limited_products , many=True)

            return Response(serializer.data)
        else:
            return Response({"message": "clothesType query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

class SimilarProduct(APIView):
    def get(self, request):
        query = request.query_params.get('category', None)
        if query:
            products = models.Product.objects.filter(category=query)
            productlist = list(products)
            random.shuffle(productlist)
            limited_products = productlist[:10]
            serializer = serializers.ProductSerializer(limited_products, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"message": "category query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

class SearchProductByTitle(APIView):
    def get(self,request):
        query = request.query_params.get('title' , None)
        if query:
            products = models.Product.objects.filter(title__icontains=query)
            serializer = serializers.ProductSerializer(products , many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "title query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

class FilterProductByCategory(APIView):

    def get(self,request):
        query = request.query_params.get('category' , None)
        if query:
            products = models.Product.objects.filter(category=query)
            serializer = serializers.ProductSerializer(products , many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "category query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)