from django.shortcuts import render
from .models import Product
from rest_framework import status
from .serializers import ProductSerializer
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from .pagination import ProductPagination

# Create your views here.
@api_view(['GET'])
def product_list(request):
    paginator=ProductPagination()
    products=Product.objects.all()
    result_page=paginator.paginate_queryset(products,request)
    if result_page is not None:
        serializer=ProductSerializer(result_page,many=True)
        return paginator.get_paginated_response(serializer.data)
    serializer=ProductSerializer(products,many=True)
    return Response(serializer.data)

def home(request):
    return HttpResponse("Hello, Welcome to Products API Project!")

@api_view(['GET'])
def product_detail(request,id):
    product=get_object_or_404(Product,id=id)
    if product is None:
        return Response(status=404)
    serializer=ProductSerializer(product)
    return Response(serializer.data)

@api_view(['POST'])
def create_product(request):
    serializer=ProductSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
def update_product(request):
    product=get_object_or_404(Product,name=request.data['name'])
    serializer=ProductSerializer(product,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_product(request):
    product=get_object_or_404(Product,name=request.data['name'])
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)