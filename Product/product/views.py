from django.shortcuts import render
# from .models import Product
from rest_framework import status
from .serializers import ProductSerializer, ProductCategorySerializer
from rest_framework.response import Response 
from django.http import HttpResponse 
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .pagination import ProductPagination
from .services import ProductService,ProductCategoryService

product_service=ProductService()
product_category_service=ProductCategoryService()

def home(request):
    return HttpResponse("Hello, Welcome to Products API Project!")

#################### PRODUCT CRUD OPERATIONS ####################

def product_list(request):
    products = product_service.list_products()
    paginator = ProductPagination()
    result_page = paginator.paginate_queryset(list(products), request)
    serializer = ProductSerializer(result_page if result_page is not None else products, many=True)
    
    if request.accepted_renderer.format == 'html' or 'text/html' in request.META.get('HTTP_ACCEPT', ''):
        result=serializer.data
        context = {
            'products': result,
            'page_obj': paginator.page,  # The paginated page object
            'paginator': paginator,   # The paginator instance
        }
        return render(request, 'product/product_list.html', context)
    
    if result_page is not None:
        return paginator.get_paginated_response(serializer.data)
    return Response(serializer.data)

def product_detail_by_id(request):
    id=request.query_params.get('id')
    product=product_service.get_product_by_id(id)
    if product is None:
        return Response(status=404)
    if "error" in product:
        return Response(product['error'], status=status.HTTP_404_NOT_FOUND)
    elif product["success"]:
        result=product_category_service.get_category_by_id(product['data']['category'])
        print(product['data']['category'])
        product['data']['category-title']=result['data']['title']
        return Response(product['data'], status=status.HTTP_200_OK)
    else:
        return Response(product['error'], status=status.HTTP_400_BAD_REQUEST)

def product_detail_by_name(request):
    name=request.query_params.get('name')
    product=product_service.get_product_by_name(name)
    if "error" in product:
        return Response(product['error'], status=status.HTTP_404_NOT_FOUND)
    elif product["success"]:
        return Response(product['data'], status=status.HTTP_200_OK)
    else:
        return Response(product['error'], status=status.HTTP_400_BAD_REQUEST)

def create_product(request):
    result=product_service.create_product(request.data)
    if result["success"]:
        return Response(result['data'], status=status.HTTP_201_CREATED)
    else:
        return Response(result['error'], status=status.HTTP_400_BAD_REQUEST)    

def update_product(request):
    result=product_service.update_product(request.data)
    if result["success"]:
        return Response(result['data'], status=status.HTTP_200_OK)
    else:
        return Response(result['error'], status=status.HTTP_400_BAD_REQUEST)

def delete_product(request):
    product_service.delete_product(request.query_params.get('name'))
    return Response(status=status.HTTP_204_NO_CONTENT)

def get_products_by_category(request):
    category=request.query_params.get('category')
    category_dict=product_category_service.get_category_by_name(category)
    if "error" in category_dict:
        return Response(category_dict['error'], status=status.HTTP_404_NOT_FOUND)
    elif category_dict["success"]:
        category_id=category_dict['data']['id']
        products=product_service.get_products_by_categoryID(category_id)
        if "error" in products:
            return HttpResponse("No products found in this category")
        else:
            products=products['data']
            paginator=ProductPagination()
            result_page=paginator.paginate_queryset(list(products),request)
            if result_page is not None: 
                serializer=ProductSerializer(result_page,many=True)
                return paginator.get_paginated_response(serializer.data)
            serializer=ProductSerializer(products,many=True)
            return Response(serializer.data)

@api_view(['GET', 'POST','DELETE','PATCH','UPDATE'])
def product_handler(request):
    if request.method == 'GET':
        if request.query_params.get('id') is not None:
            # print("id present in params")
            return product_detail_by_id(request)
        elif request.query_params.get('name') is not None:
            return product_detail_by_name(request)
        elif request.query_params.get('category') is not None:
            return get_products_by_category(request)
        elif (not request.query_params) or (request.query_params.get('page') is not None):
            return product_list(request)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        return create_product(request)
    elif request.method == 'PATCH':
        return update_product(request)
    elif request.method == 'DELETE':
        return delete_product(request)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

#################### CATEGORY CRUD OPERATIONS ####################

def create_product_category(request):
    data=request.data
    response=product_category_service.create_product_category(data)
    if(response['success']):
        return Response(response['data'],status=status.HTTP_201_CREATED)
    else:
        return Response(response['error'],status=status.HTTP_400_BAD_REQUEST)

def update_product_category(request):
    data=request.data
    response=product_category_service.update_category(data)
    if(response['success']):
        return Response(response['data'],status=status.HTTP_200_OK)
    else:
        return Response(response['error'],status=status.HTTP_400_BAD_REQUEST)
    
def product_category_list(request):
    categories=product_category_service.list_product_categories()
    paginator=ProductPagination()
    result_page=paginator.paginate_queryset(list(categories),request)
    if result_page is not None: 
        serializer=ProductCategorySerializer(result_page,many=True)
        return paginator.get_paginated_response(serializer.data)
    serializer=ProductCategorySerializer(categories,many=True)
    return Response(serializer.data)

def get_category_by_name(request):
    category_name=request.query_params.get('category')
    category=product_category_service.get_category_by_name(category_name)
    if "error" in category:
        return Response(category['error'], status=status.HTTP_404_NOT_FOUND)
    elif category["success"]:
        return Response(category['data'], status=status.HTTP_200_OK)
    else:
        return Response(category['error'], status=status.HTTP_400_BAD_REQUEST)
    
def delete_product_category(request):
    category_title=request.query_params.get('category')
    response=product_category_service.delete_product_category(category_title)
    if(response['success']):
        return Response(response['message'],status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(response['error'],status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST','PATCH','UPDATE','DELETE'])
def category_handler(request):
    if request.method == 'GET':
        if not request.query_params:
            return product_category_list(request)
        elif request.query_params.get('category') is not None:
            return get_category_by_name(request)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        return create_product_category(request)
    elif request.method == 'PATCH':
        return update_product_category(request)
    elif request.method == 'DELETE':
        return delete_product_category(request)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)