from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

# Create your views here.
@api_view(["GET"])
def products_list(request):
    cache_key = "product_list"

    if not cache.get(cache_key):
        print("cache miss")
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        json_response = serializer.data
        cache.set(cache_key, json_response, 180)

    response_data = cache.get(cache_key)

    return Response(response_data)