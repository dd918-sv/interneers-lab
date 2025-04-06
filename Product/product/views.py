from django.shortcuts import render
# from .models import Product
from rest_framework import status
from .serializers import ProductSerializer, ProductCategorySerializer
from rest_framework.response import Response 
from django.http import HttpResponse 
from rest_framework.decorators import api_view
from .pagination import ProductPagination
from .services import ProductService,ProductCategoryService

product_service=ProductService()
product_category_service=ProductCategoryService()

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
    id=request.query_params.get('id')
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
    name=request.query_params.get('name')
    product=product_service.get_product_by_name(name)
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
    product_service.delete_product(request.query_params.get('name'))
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def create_product_category(request):
    data=request.data
    response=product_category_service.create_product_category(data)
    if(response['success']):
        return Response(response['data'],status=status.HTTP_201_CREATED)
    else:
        return Response(response['error'],status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_product_category(request):
    data=request.data
    response=product_category_service.update_category(data)
    if(response['success']):
        return Response(response['data'],status=status.HTTP_200_OK)
    else:
        return Response(response['error'],status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def product_category_list(request):
    categories=product_category_service.list_product_categories()
    paginator=ProductPagination()
    result_page=paginator.paginate_queryset(list(categories),request)
    if result_page is not None: 
        serializer=ProductCategorySerializer(result_page,many=True)
        return paginator.get_paginated_response(serializer.data)
    serializer=ProductCategorySerializer(categories,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_products_by_category(request):
    category=request.query_params.get('category')
    products=product_category_service.get_products_by_category(category)
    paginator=ProductPagination()
    result_page=paginator.paginate_queryset(list(products),request)
    if result_page is not None: 
        serializer=ProductSerializer(result_page,many=True)
        return paginator.get_paginated_response(serializer.data)
    serializer=ProductSerializer(products,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_category_by_name(request):
    category_name=request.query_params.get('category')
    category=product_category_service.get_category_by_name(category_name)
    if "error" in category:
        return Response(category['error'], status=status.HTTP_404_NOT_FOUND)
    elif category["success"]:
        return Response(category['data'], status=status.HTTP_200_OK)
    else:
        return Response(category['error'], status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def delete_product_category(request):
    category_title=request.query_params.get('category')
    response=product_category_service.delete_product_category(category_title)
    if(response['success']):
        return Response(response['message'],status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(response['error'],status=status.HTTP_400_BAD_REQUEST)


