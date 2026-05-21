import profile

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from core import views
from django.contrib.auth import views as auth_views
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

    path('index/', index, name='index'),
    path('blog/<int:pk>/', blog_detail, name='blog_detail'),
    path('blogs/', blog_list, name='blog_list'),
    path('product/<int:id>/', product_detail, name='product_detail'),
    path('cart/', cart_view, name='cart'),
    path('category/<str:category_name>/', category_product, name='category_product'),
    path('contact/', contact, name='contact'),
    path('ReportOrder/', ReportOrder, name='ReportOrder'),
    path('ReportOrderByShift/', ReportOrderByShift, name='ReportOrderByShift'),
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path("register/", views.register,name="register"),
    path('profile/', profile, name='profile'),
    path('logout/',auth_views.LogoutView.as_view(next_page='index'),name='logout'),

]