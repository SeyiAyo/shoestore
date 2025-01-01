from rest_framework import serializers
from .models import Category, Product, Size, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'size', 'gender', 'quantity']

class ProductSerializer(serializers.ModelSerializer):
    sizes = SizeSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'category_name', 
                 'image', 'in_stock', 'brand', 'sku', 'sizes']

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    size_info = serializers.CharField(source='size.__str__', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'size', 'size_info', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'user_email', 'created_at', 'updated_at', 'status', 
                 'status_display', 'shipping_address', 'total_amount', 'items']
        read_only_fields = ['user', 'created_at', 'updated_at']
