from rest_framework import viewsets, permissions, generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Customer, Seller, Product, Order, PlatformApiCall
from .serializers import CustomerSerializer, SellerSerializer, ProductSerializer, OrderSerializer, PlatformApiCallSerializer, RegisterSerializer,UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db import IntegrityError
from rest_framework import status
from .permissions import IsCustomerOwner  # Import the custom permission class

# Mixin for PlatformApiCall logging
class PlatformApiCallMixin:
    def log_api_call(self, serializer):
        PlatformApiCall.objects.create(
            user=self.request.user,
            requested_url=self.request.build_absolute_uri(),
            requested_data=self.request.data,
            response_data=serializer.data
        )

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self.log_api_call(serializer)

    def perform_update(self, serializer):
        super().perform_update(serializer)
        self.log_api_call(serializer)

    def perform_destroy(self, instance):
        response_data = {'detail': f'{instance} deleted'}
        PlatformApiCall.objects.create(
            user=self.request.user,
            requested_url=self.request.build_absolute_uri(),
            requested_data=self.request.data,
            response_data=response_data
        )
        super().perform_destroy(instance)


# Register view for creating new users
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

# Product ViewSet with CRUD operations and logging
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response({"detail": "A product with this name already exists."}, status=status.HTTP_400_BAD_REQUEST)
# Order ViewSet with CRUD operations, restricted to the authenticated user's orders, and logging
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Filter and search functionality
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['products__name']  # Filter by product name
    search_fields = ['products__name']     # Search by product name
    ordering_fields = ['amount', 'created_at']  # Fields for ordering

    def get_queryset(self):
        # Filter orders by the authenticated user
        queryset = Order.objects.filter(customer__user=self.request.user)

        # Use select_related to optimize related object retrieval for foreign key relationships
        queryset = queryset.select_related('customer', 'seller')

        # Use prefetch_related to optimize retrieval of many-to-many relationships
        queryset = queryset.prefetch_related('products')
        # Sorting and top results
        sort_by = self.request.query_params.get('sort_by', None)
        top_n = self.request.query_params.get('top_n', None)

        if sort_by:
            if sort_by == 'ascending':
                queryset = queryset.order_by('created_at')
            elif sort_by == 'descending':
                queryset = queryset.order_by('-created_at')

        if top_n == '5':
            queryset = queryset[:5]  # Limit to top 5 results

        return queryset

        # Return the optimized queryset
# Customer ViewSet
class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomerOwner]

    def get_queryset(self):
        # Filter queryset to only include the current user's customer data
        return Customer.objects.filter(user=self.request.user)

# Seller ViewSet
class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


# PlatformApiCall ViewSet (Read-only, Admin access only)
class PlatformApiCallViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PlatformApiCall.objects.all()
    serializer_class = PlatformApiCallSerializer
    permission_classes = [permissions.IsAdminUser]
