from rest_framework import viewsets, generics, permissions
from .serializers import*
from django.shortcuts import render,get_object_or_404
from .models import *
import json
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser,IsAuthenticated
from .models import AccessToken
from .authentication import QueryParamAccessTokenAuthentication

from .models import AccessToken
import uuid
from rest_framework import status

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Username and password are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)
        if user is None:
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Deactivate old tokens
        AccessToken.objects.filter(user=user, is_active=True).update(is_active=False)

        # Create new token
        token_str = uuid.uuid4().hex
        token_obj = AccessToken.objects.create(user=user, token=token_str, is_active=True)

        return Response({'access_token': token_obj.token})
def ReportOrder(request):
    return render(request, 'core/ReportOrder.html')
def cart_view(request):
    qrcodes = QRCode.objects.all()
    return render(request, 'cart.html', {'qrcodes': qrcodes})
def checkout(request):
    if request.method == 'POST':
        # Handle both JSON and form-data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            files = {}
        else:
            data = request.POST
            files = request.FILES
        customerName = data.get('customerName')
        customerPhone = data.get('customerPhone')
        totalAmount = data.get('totalAmount')
        items = json.loads(data.get('items', '[]'))

        # Create order
        order = Order.objects.create(
            customerName=customerName,
            customerPhone=customerPhone,
            totalAmount=totalAmount,
        )

        # Save items
        for item in items:
            OrderItem.objects.create(
                order=order,
                productName=item['productName'],
                price=item['price'],
                quantity=item['qty']
            )

        # Handle QR code (upload or selection)
        qr_preview = "No QR code available."
        qr_file = files.get('QRCodeInvoice')
        qr_selected_id = data.get('QRCodeInvoice')

        if qr_file:  # Uploaded file
            order.QRCodeInvoice.save(qr_file.name, qr_file)
            qr_preview = request.build_absolute_uri(order.QRCodeInvoice.url)

        elif qr_selected_id:  # Selected from dropdown
            try:
                qr = QRCode.objects.get(pk=qr_selected_id)
                order.QRCodeInvoice = qr.qrImage
                qr_preview = request.build_absolute_uri(qr.qrImage.url)
            except QRCode.DoesNotExist:
                pass

        order.save()

        return JsonResponse({
            'id': order.id,
            'customerName': order.customerName,
            'customerPhone': order.customerPhone,
            'totalAmount': order.totalAmount,
            'items': list(order.items.values('productName', 'price', 'quantity')),
            'qrcodes': qr_preview
        })

    return JsonResponse({'error': 'POST method required'}, status=400)
def contact(request):
    return render(request, 'core/contact-us.html')   
def category_product(request, category_name):
    best_sellers = Product.objects.filter(is_best_seller=True)
    popular_products = Product.objects.filter(is_popular=True)
    new_arrivals = Product.objects.filter(is_new_arrival=True)
    blogs = Blog.objects.all()
    banners = SmallBanner.objects.all()
    hero = HeroSection.objects.first()
    category = get_object_or_404(Category, categoryName__iexact=category_name)
    filtered_products = Product.objects.filter(category=category)
    return render(request, 'core/category_product.html', {
        'best_sellers': best_sellers,
        'popular_products': popular_products,
        'new_arrivals': new_arrivals,
        'blogs': blogs,
        'banners': banners,
        'hero': hero,
        'category': category,
        'filtered_products': filtered_products,
    })

def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'core/blog_list.html', {'blogs': blogs})

def ReportOrderByShift(request):
    return render(request, 'core/ReportOrderByShift.html')
               
def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'core/blog_detail.html', {'blog': blog})
def index(request):
    best_sellers = Product.objects.filter(is_best_seller=True)
    popular_products = Product.objects.filter(is_popular=True)
    new_arrivals = Product.objects.filter(is_new_arrival=True)
    blogs = Blog.objects.all()
    banners = SmallBanner.objects.all()
    hero = HeroSection.objects.first()

    return render(request, 'core/index.html', {
        'best_sellers': best_sellers,
        'popular_products': popular_products,
        'new_arrivals': new_arrivals,
        'blogs': blogs,
        'banners': banners,
        'hero': hero,
    })
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    details = product.productdetail_set.all()
    size_options = SizeOption.objects.all()
    return render(request, 'core/product_detail.html', {'product': product, 'details': details, 'size_options': size_options})


def cart_view(request):
    order = Order.objects.order_by('-orderDate').first()
    qrcodes = QRCode.objects.all()
    items = order.items.all() if order else []
    total_items = sum(item.quantity for item in items) if items else 0

    return render(request, 'core/cart.html', {
        'order': order,
        'items': items,
        'total_items': total_items,
        'qrcodes': qrcodes,  
    })

  
class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
   
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    authentication_classes = [QueryParamAccessTokenAuthentication]
    permission_classes = [AllowAny]  # or use custom permission

    def get_queryset(self):

        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
    
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('categoryID')
        if category_id:
            queryset = queryset.filter(categoryID_id=category_id)
        return queryset
class ProductDetailViewSet(viewsets.ModelViewSet):
    queryset = ProductDetail.objects.all()
    serializer_class = ProductDetailSerializer

    def get_queryset(self):
        product_id = self.request.query_params.get('productID')
        if product_id:
            return ProductDetail.objects.filter(productID=product_id)
        return ProductDetail.objects.all()

# Orders views - user must be authenticated

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
   
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogSerializer
class QRCodeViewSet(viewsets.ModelViewSet):
    queryset = QRCode.objects.all()
    serializer_class = QRCodeSerializer
