from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Category, Product, Size, Order, OrderItem
from .serializers import (
    CategorySerializer, ProductSerializer, SizeSerializer,
    OrderSerializer, OrderItemSerializer
)
from .debug import log_debug, log_error, api_error_response

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def list(self, request, *args, **kwargs):
        try:
            log_debug('Fetching categories', {'user': request.user.username if request.user.is_authenticated else 'anonymous'})
            return super().list(request, *args, **kwargs)
        except Exception as e:
            log_error('Error fetching categories', e)
            return api_error_response('Failed to fetch categories', status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'brand']
    ordering_fields = ['price', 'created_at', 'rating']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'add_size']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        try:
            queryset = Product.objects.all()
            category = self.request.query_params.get('category', None)
            min_price = self.request.query_params.get('min_price', None)
            max_price = self.request.query_params.get('max_price', None)
            brand = self.request.query_params.get('brand', None)

            log_debug('Filtering products', {
                'category': category,
                'min_price': min_price,
                'max_price': max_price,
                'brand': brand
            })

            if category:
                queryset = queryset.filter(category_id=category)
            if min_price:
                queryset = queryset.filter(price__gte=min_price)
            if max_price:
                queryset = queryset.filter(price__lte=max_price)
            if brand:
                queryset = queryset.filter(brand__iexact=brand)

            return queryset
        except Exception as e:
            log_error('Error filtering products', e)
            return Product.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            log_debug('Fetching products', {'params': dict(request.query_params)})
            return super().list(request, *args, **kwargs)
        except Exception as e:
            log_error('Error fetching products', e)
            return api_error_response('Failed to fetch products', status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def add_size(self, request, pk=None):
        try:
            product = self.get_object()
            serializer = SizeSerializer(data=request.data)
            
            log_debug('Adding size to product', {
                'product_id': pk,
                'size_data': request.data
            })
            
            if serializer.is_valid():
                serializer.save(product=product)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            log_error('Invalid size data', extra={'errors': serializer.errors})
            return api_error_response('Invalid size data', extra={'errors': serializer.errors})
            
        except Exception as e:
            log_error('Error adding size to product', e)
            return api_error_response('Failed to add size', status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'add_item']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user)
        return Order.objects.none()

    def perform_create(self, serializer):
        try:
            log_debug('Creating order', {'user': self.request.user.username})
            serializer.save(user=self.request.user)
        except Exception as e:
            log_error('Error creating order', e)
            raise

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        try:
            order = self.get_object()
            product = get_object_or_404(Product, pk=request.data.get('product'))
            size = get_object_or_404(Size, pk=request.data.get('size'))
            
            log_debug('Adding item to order', {
                'order_id': pk,
                'product_id': product.id,
                'size_id': size.id,
                'quantity': request.data.get('quantity', 1)
            })
            
            if size.quantity < request.data.get('quantity', 1):
                log_error('Insufficient stock', extra={
                    'available': size.quantity,
                    'requested': request.data.get('quantity', 1)
                })
                return api_error_response(
                    'Not enough stock available',
                    extra={'available': size.quantity}
                )
            
            item_data = {
                'product': product.id,
                'size': size.id,
                'quantity': request.data.get('quantity', 1),
                'price': product.price
            }
            
            serializer = OrderItemSerializer(data=item_data)
            if serializer.is_valid():
                serializer.save(order=order)
                # Update stock
                size.quantity -= item_data['quantity']
                size.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            log_error('Invalid order item data', extra={'errors': serializer.errors})
            return api_error_response('Invalid order item data', extra={'errors': serializer.errors})
            
        except Exception as e:
            log_error('Error adding item to order', e)
            return api_error_response('Failed to add item to order', status.HTTP_500_INTERNAL_SERVER_ERROR)
