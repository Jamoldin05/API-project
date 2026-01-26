
from rest_framework import generics
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .permissions import CanUpdate4Hours
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from django.core.cache import cache


class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            {"detail": "Logout muvaffaqiyatli bajarildi"},
            status=status.HTTP_200_OK
        )


class ProductViewSet(generics.RetrieveDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [CanUpdate4Hours]



class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        cache_key = 'category_list'
        data = cache.get(cache_key)

        if not data:
            response = super().get(request, *args, **kwargs)
            cache.set(cache_key, response.data, timeout=60 * 10) 
            return response

        return Response(data)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.select_related('category').prefetch_related('images')
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        cache_key = 'product_list'
        data = cache.get(cache_key)

        if not data:
            response = super().get(request, *args, **kwargs)
            cache.set(cache_key, response.data, timeout=60 * 5)  
            return response

        return Response(data)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.prefetch_related('images')
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        cache_key = f'product_detail_{pk}'
        data = cache.get(cache_key)

        if not data:
            response = super().get(request, *args, **kwargs)
            cache.set(cache_key, response.data, timeout=60 * 5)
            return response

        return Response(data)
