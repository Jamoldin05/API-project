from django.urls import path
from .views import (
    CategoryListCreateView,
    CategoryDetailView,
    ProductListCreateView,
    ProductDetailView,
    ProductViewSet,
    LogoutAPIView,
)



urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('products/', ProductListCreateView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]


