from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, OrderViewSet, CustomerViewSet, SellerViewSet, PlatformApiCallViewSet, RegisterView,LoginView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')  # Add basename here
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'sellers', SellerViewSet, basename='seller')
router.register(r'platform-api-calls', PlatformApiCallViewSet, basename='platformapicall')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
     path('login/', LoginView.as_view(), name='login'),
]


