from django.urls import path 
from . import views

urlpatterns = [
    path('toggle/',views.ToggleWishList.as_view(),name='add-remove-from'),
    path('me/',views.GetWishlist.as_view(), name='Get-Wishlist')
]
