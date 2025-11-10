from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from . import models, serializers


class AddAddress(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        # إلغاء تعيين أي عنوان افتراضي حالي إذا تم إرسال العنوان الجديد كـ default
        if data.get('isDefault', False):
            models.Address.objects.filter(userId=request.user).update(isDefault=False)

        user_address = models.Address.objects.create(
            userId=request.user,
            lat=data['lat'],
            lng=data['lng'],
            isDefault=data.get('isDefault', False),
            address=data['address'],
            phone=data['phone'],
            addressType=data['addressType'],
        )

        return Response({'message': 'Address added successfully'}, status=status.HTTP_201_CREATED)


class GetUserAddress(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        address = models.Address.objects.filter(userId=request.user)
        serializer = serializers.AddressSerializer(address, many=True)
        return Response(serializer.data)


class GetDefaultAddrss(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        address = models.Address.objects.filter(userId=request.user, isDefault=True).first()
        if address:
            serializer = serializers.AddressSerializer(address)
            return Response(serializer.data)
        else:
            return Response({'message': 'No default address found'}, status=status.HTTP_404_NOT_FOUND)


class DeleteAdrees(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        address_id = request.query_params.get('id')
        if not address_id:
            return Response({'message': 'No id provided'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        try:
            address_item = models.Address.objects.get(id=address_id, userId=user)

            with transaction.atomic():
                # لو العنوان اللي هيتم حذفه هو الافتراضي
                if address_item.isDefault:
                    other_address = models.Address.objects.filter(userId=user).exclude(id=address_id)
                    if other_address.exists():
                        new_default = other_address.first()
                        new_default.isDefault = True
                        new_default.save()
                    else:
                        return Response(
                            {'message': 'You cannot delete the only default address.'},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                address_item.delete()
                return Response({'message': 'Address deleted successfully'}, status=status.HTTP_200_OK)

        except models.Address.DoesNotExist:
            return Response({'message': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)


class SetDefaultAddress(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        address_id = request.query_params.get('id')
        if not address_id:
            return Response({'message': 'No id provided'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        try:
            with transaction.atomic():
                # أولًا نحط كل العناوين isDefault=False
                models.Address.objects.filter(userId=user).update(isDefault=False)

                # بعد كده نجيب العنوان المطلوب ونخليه افتراضي
                address = models.Address.objects.get(id=address_id, userId=user)
                address.isDefault = True
                address.save()

            return Response({'message': 'Default address updated successfully'}, status=status.HTTP_200_OK)

        except models.Address.DoesNotExist:
            return Response({'message': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)
