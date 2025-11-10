from django.urls import path
from . import views

urlpatterns = [
    path('addresslist/',views.GetUserAddress.as_view(),name='user-address'),
    path('add/',views.AddAddress.as_view(), name='add-address'),
    path('default/',views.SetDefaultAddress.as_view() , name='default-address'),
    path('delete/',views.DeleteAdrees.as_view(),name='delete-address'),
    path('me/',views.GetDefaultAddrss.as_view(),name='get-default-address')
]
