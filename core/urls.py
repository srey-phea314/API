from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from django.shortcuts import render
from django.contrib import admin
from . import views 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('products', ProductViewSet)
router.register('blogs', BlogViewSet)
router.register('orders', OrderViewSet)
router.register('qrcodes', QRCodeViewSet)
router.register('product-detail', ProductDetailViewSet)
router.register('product-images', ProductImageViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('index', index, name='index'), 
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('blogs/', views.blog_list, name='blog_list'), 
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('cart/', cart_view, name='cart'),
    path('category/<str:category_name>/', views.category_product, name='category_product'),
    path('contact/', views.contact, name='contact'), 
    path('ReportOrder/', ReportOrder, name='ReportOrder'),
    path('ReportOrderByShift/', ReportOrderByShift, name='ReportOrderByShift'),
    path('api/login/', LoginAPIView.as_view(), name='login'),
   
]

