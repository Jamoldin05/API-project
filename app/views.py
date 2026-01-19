
from rest_framework import generics
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .permissions import CanUpdate4Hours
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status


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


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.select_related('category').prefetch_related('images')
    serializer_class = ProductSerializer



class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.prefetch_related('images')
    serializer_class = ProductSerializer


