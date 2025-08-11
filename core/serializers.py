from rest_framework import serializers
from .models import *
import json
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        field ='__all__'
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'categoryName']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # nested category
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Product
        fields = '__all__'
class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = '__all__'
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['productName', 'price', 'quantity']
class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'
    def get_items(self, obj):
        items = obj.items.all()
        return OrderItemSerializer(items, many=True).data

    def create(self, validated_data):
        request = self.context['request']
        items_json = request.data.get('items')
        items_data = json.loads(items_json) if items_json else []
        # Pop items key out, rest is for Order creation (QRCodeInvoice will be in validated_data as file)
        validated_data.pop('items', None)
        order = Order.objects.create(**validated_data)

        for item in items_data:
            if 'qty' in item:
                item['quantity'] = item.pop('qty')
            OrderItem.objects.create(order=order, **item)  # Move this line inside the loop


        return order
class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = '__all__'
