from django.contrib import admin
from django.urls import path , include
from core import views

urlpatterns = [
    path('categories/' , views.CategoryList.as_view() , name='category-list'),
    path('home-categories/' , views.HomeCategoryList.as_view() , name='home-category-list'),
    path('',views.ProductList.as_view() , name='product-list'),
    path('popular/',views.PopularProductList.as_view() , name='popular-product-list'),
    path('byType/',views.ProductListByClothesType.as_view() , name='product-list-by-type'),
    path('search/',views.SearchProductByTitle.as_view() , name='search'),
    path('category/',views.FilterProductByCategory.as_view() , name='product-by-category'),
    path('recommedations/', views.SimilarProduct.as_view(), name='similar-products'),
]
