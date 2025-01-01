from rest_framework import serializers
from .models import Category, Product, Size, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='pk', read_only=True)
    imageUrl = serializers.SerializerMethodField()
    sizes = serializers.SerializerMethodField()
    colors = serializers.SerializerMethodField()
    category = serializers.CharField(source='category.name')
    price = serializers.SerializerMethodField()
    reviewCount = serializers.IntegerField(source='review_count')

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'imageUrl',
            'sizes', 'category', 'brand', 'colors', 'rating', 'reviewCount'
        ]

    def get_imageUrl(self, obj):
        if obj.image:
            return obj.image
        return 'https://images.unsplash.com/photo-1542291026-7eec264c27ff'  # Default image

    def get_sizes(self, obj):
        return list(obj.available_sizes)

    def get_colors(self, obj):
        return obj.available_colors

    def get_price(self, obj):
        return float(obj.price)

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'size', 'gender', 'quantity']

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    size_info = serializers.CharField(source='size.size', read_only=True)
    unit_price = serializers.DecimalField(source='price', max_digits=10, decimal_places=2)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'size', 'size_info', 'quantity', 'unit_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    total = serializers.DecimalField(source='total_amount', max_digits=10, decimal_places=2)

    class Meta:
        model = Order
        fields = [
            'id', 'user_email', 'created_at', 'status',
            'status_display', 'shipping_address', 'total', 'items'
        ]
        read_only_fields = ['created_at']
