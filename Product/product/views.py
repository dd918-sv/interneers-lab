from django.shortcuts import render
# from .models import Product
from rest_framework import status
from .serializers import ProductSerializer
from rest_framework.response import Response 
from django.http import HttpResponse
from rest_framework.decorators import api_view
from .pagination import ProductPagination
from .services import ProductService

product_service=ProductService()


def home(request):
    return HttpResponse("Hello, Welcome to Products API Project!")

@api_view(['GET'])
def product_list(request):
    products=product_service.list_products()
    paginator=ProductPagination()
    result_page=paginator.paginate_queryset(list(products),request)
    if result_page is not None: 
        serializer=ProductSerializer(result_page,many=True)
        return paginator.get_paginated_response(serializer.data)
    serializer=ProductSerializer(products,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail_by_id(request):
    id=request.data['id']
    product=product_service.get_product_by_id(id)
    if product is None:
        return Response(status=404)
    if "error" in product:
        return Response(product['error'], status=status.HTTP_404_NOT_FOUND)
    elif product["success"]:
        return Response(product['data'], status=status.HTTP_200_OK)
    else:
        return Response(product['error'], status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def product_detail_by_name(request):
    product=product_service.get_product_by_name(request.data['name'])
    if "error" in product:
        return Response(product['error'], status=status.HTTP_404_NOT_FOUND)
    elif product["success"]:
        return Response(product['data'], status=status.HTTP_200_OK)
    else:
        return Response(product['error'], status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_product(request):
    result=product_service.create_product(request.data)
    if result["success"]:
        return Response(result['data'], status=status.HTTP_201_CREATED)
    else:
        return Response(result['error'], status=status.HTTP_400_BAD_REQUEST)    
@api_view(['PATCH'])
def update_product(request):
    result=product_service.update_product(request.data)
    if result["success"]:
        return Response(result['data'], status=status.HTTP_200_OK)
    else:
        return Response(result['error'], status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_product(request):
    product_service.delete_product(request.data)
    return Response(status=status.HTTP_204_NO_CONTENT)