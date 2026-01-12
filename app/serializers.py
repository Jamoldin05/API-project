from rest_framework import serializers
from .models import Category, Product, Image



class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']



class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True) 
    image_count = serializers.SerializerMethodField()    

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'images', 'image_count']

    def get_image_count(self, obj):
        return obj.images.count()




class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'product_count', 'products']

    def get_product_count(self, obj):
        return obj.products.count()
