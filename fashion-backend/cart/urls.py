from django.urls import path
from . import views

urlpatterns = [
    path('me/',views.GetUserCart,name='get-user-cart'),
    path('add/', views.AddItemCart,name='add-to-cart'),
    path('count/',views.CartCount,name='count'),
    path('delete/',views.RemoveItemFromCart,name='delete'),
    path('update/',views.UpdateCartItemQuantity,name='update'),
]
