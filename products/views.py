from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from products.models import Product
from products.serializers import ProductSerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
def add_product_list(request):
    if request.method == 'POST':
        product_data = JSONParser().parse(request)
        product_serializer = ProductSerializer(data=product_data)
        if product_serializer.is_valid():
            product_serializer.save()
            return JsonResponse(product_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_list_products(request):
    products = Product.objects.filter()
    if request.method == 'GET':
        products_serializer = ProductSerializer(products, many=True)
        return JsonResponse(products_serializer.data, safe=False)
