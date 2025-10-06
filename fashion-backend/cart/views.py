from django.shortcuts import render
from .models import Product , Cart
from .serializers import CartSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import generics , status
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

class AddItemCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        user = request.user
        data = request.data
        try:
            product = Product.objects.get(id=data['product'])
        except Product.DoesNotExist:
            return Response({"message":"Product doesn't exist"} , status=status.HTTP_404_NOT_FOUND)
        try:
            cart_item = Cart.objects.get(
                userid=user,
                product=product,
                color = data['color'],
                size = data['size']
            )
            cart_item.quantity += data.get('quantity',1)
            cart_item.save()
            return Response({'message':'Item updated sucessfully'})
        except Cart.DoesNotExist:
            Cart.objects.create(
                userid = user,
                product=product,
                color = data['color'],
                size = data['size'],
                quantity = data.get('quantity' ,1),
            )
            return Response({'message':'Item add succssfully'},status=status.HTTP_201_CREATED)

class RemoveItemFromCart(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self,request):
        user = request.user
        cart_id = request.query_params.get('id')
        
        if not cart_id:
            return Response({"message":'Cart id is required'}, status=status.HTTP_404_NOT_FOUND)
        
        
        cart_item = Cart.objects.filter(userid=user)
        
        if not cart_item.filter(id=cart_id).exists():
            return Response({"message":"Cart item does not exist"}, status= status.HTTP_404_NOT_FOUND)

        cart_item.filter(id=cart_id).delete()
        return Response({"message":"Item removed Successfully"}, status=status.HTTP_204_NO_CONTENT)


class CartCount(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        cart_count = Cart.objects.filter(userid=user).count()
        return Response({'cart_count':cart_count},status=status.HTTP_200_OK)
