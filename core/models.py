from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import uuid

class AccessToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True, default=uuid.uuid4().hex)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.token[:10]}..."

    def save(self, *args, **kwargs):
        # Ensure token is generated if not provided
        if not self.token:
            self.token = uuid.uuid4().hex
        super().save(*args, **kwargs)
class Category(models.Model):
    categoryName = models.CharField(max_length=200, null=True)
    categoryImage = models.ImageField(upload_to='images/Categories/',null=True,blank=True)
    def __str__(self):         
        return f'{self.id} - {self.categoryName}'
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    original_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='products/')
    rating = models.IntegerField(null=True, blank=True) 
    is_on_sale = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)  
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])
class ProductDetail(models.Model):
    productDetailName = models.CharField(max_length=200, null=True)
    productID = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)    
    Information = RichTextUploadingField(null=True)   
    Reviews = RichTextUploadingField(null=True)    
    productDetailDate = models.DateTimeField(auto_now_add=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    original_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)  
    available = models.BooleanField(default=True)

    # NEW FIELDS:
    skin_type = models.CharField(max_length=200, null=True, blank=True)
    shelf_life = models.CharField(max_length=100, null=True, blank=True)
    application_time = models.CharField(max_length=100, null=True, blank=True)
    packaging = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):         
        return f'{self.productID.name} - {self.productDetailName}'
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.product.name} Image"

class SizeOption(models.Model):
    product = models.ForeignKey(Product, related_name='sizes', on_delete=models.CASCADE)
    size_label = models.CharField(max_length=50) 
    is_color = models.BooleanField(default=False) 
    color_hex = models.CharField(max_length=7, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.size_label}"


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
class Order(models.Model):
    customerName = models.CharField(max_length=100)
    customerPhone = models.CharField(max_length=20)
    orderDate = models.DateTimeField(auto_now_add=True)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2)
    QRCodeInvoice = models.ImageField(upload_to='images/QRCodeInvoice/', null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} - {self.customerName}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    productName = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    
    def subtotal(self):
        return self.quantity * self.price
class HeroSection(models.Model):
    image = models.ImageField(upload_to='hero/', null=True, blank=True)
from django.db import models
class BestSellerProduct(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    description = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=5)  # rating from 0 to 5

    def __str__(self):
        return self.name
class SmallBanner(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='banners/')
    

    def __str__(self):
        return self.title

class NewArrivalProduct(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    is_on_sale = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
class PopularProduct(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    original_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='products/')
    rating = models.PositiveSmallIntegerField(default=5)  # 1 to 5 stars
    is_on_sale = models.BooleanField(default=False)

    def __str__(self):
        return self.name
class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='blog_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', args=[str(self.id)])

class QRCode(models.Model):
    qrName = models.CharField(max_length=100)
    qrImage = models.ImageField(upload_to='images/qrcodes/')
    def __str__(self): return self.qrName 
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.full_name or self.user.username