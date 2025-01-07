from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views.profile_views import ProfileView
from .views.product_views import CategoryViewSet, ProductViewSet
from .views.order_views import OrderViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # Profile URLs
    path('api/profile/', ProfileView.as_view(), name='profile'),
]
