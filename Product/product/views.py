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
import time

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
    
    result=serializer.data
    context = {
        'products': serializer.data,
        'current_page': paginator.page.number,
        'total_pages': paginator.page.paginator.num_pages,
        'total_items': paginator.page.paginator.count,
        'next_page': paginator.get_next_link(),
        'previous_page': paginator.get_previous_link(),
    }
    if request.accepted_renderer.format == 'html' or 'text/html' in request.META.get('HTTP_ACCEPT', ''):
        context['page_obj'] = paginator.page
        context['paginator'] = paginator
        return render(request, 'product/product_list.html', context)
        
    
    if result_page is not None:
        return Response(context)
    return Response({'products':serializer.data})

def product_detail_by_id(request):
     
    id=request.query_params.get('id')
    product=product_service.get_product_by_id(id)
    if product is None:
        return Response({'success':False,'error':'Product Not Found'},status=status.HTTP_404_NOT_FOUND)
    if "error" in product:
        return Response({'success':False,'error':product['error']}, status=status.HTTP_404_NOT_FOUND)
    elif product["success"]:
        result=product_category_service.get_category_by_id(product['data']['category'])
        # print(product['data'])
        product['data']['category-title']=result['data']['title']
        return Response({'success':True,'data':product['data']}, status=status.HTTP_200_OK)
    else:
        return Response({'success':True,'error':product['error']}, status=status.HTTP_400_BAD_REQUEST)

def product_detail_by_name(request):
     
    name=request.query_params.get('name')
    product=product_service.get_product_by_name(name)
    if "error" in product:
        return Response({'success':False,'error':product['error']}, status=status.HTTP_404_NOT_FOUND)
    elif product["success"]:
        return Response({'success':True,'data':product['data']}, status=status.HTTP_200_OK)
    else:
        return Response({'success':True,'error':product['error']}, status=status.HTTP_400_BAD_REQUEST)

def create_product(request):
    if(('category' not in request.data)):
        return Response({'success':False,'error':'Category is a mandatory field.'},status=status.HTTP_400_BAD_REQUEST)
    if('name' not in request.data):
        return Response({'success':False,'error':'Name is a mandatory field.'},status=status.HTTP_400_BAD_REQUEST)

    result=product_service.create_product(request.data)
    if result["success"]:
        return Response({'success':True,'data':result['data']}, status=status.HTTP_201_CREATED)
    else:
        return Response({'success':False,'error':result['error']}, status=status.HTTP_400_BAD_REQUEST)    

def update_product(request):
    if('category-title' in request.data):
        category=product_category_service.get_category_by_name(request.data['category-title'])
        if(category['success']==False): 
            return Response({'success':False,'error':'Category Not Found'},status=status.HTTP_404_NOT_FOUND)
        request.data['category']=category['data']['id']
        
    result=product_service.update_product(request.data)
    if result["success"]:
        return Response(result, status=status.HTTP_200_OK)
    else:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

def delete_product(request):
    product_service.delete_product(request.query_params.get('name'))
    return Response(status=status.HTTP_204_NO_CONTENT)
 
def get_products_by_category(request):
     
    category_id=request.query_params.get('category')

    if category_id is None:
        category_title=request.query_params.get('title')
        print(category_title)
        if category_title is None:
            return Response({'success':False,'error':'Category ID or Title is required'},status=status.HTTP_400_BAD_REQUEST)
        category=product_category_service.get_category_by_name(category_title)
        if category['success']==False:
            return Response({'success':False,'error':'Category Not Found'},status=status.HTTP_404_NOT_FOUND)
        category_id=category['data']['id']


    products=product_service.get_products_by_categoryID(category_id)
    # print(products)
    if "error" in products:
        # print(products['error'])
        return Response(products)
    else:
        paginator=ProductPagination()
        result_page=paginator.paginate_queryset(list(products['data']),request)
        serializer=ProductSerializer(result_page,many=True)
        result=serializer.data
        context = {
            'success':True,
            'products': serializer.data,
            'current_page': paginator.page.number,
            'total_pages': paginator.page.paginator.num_pages,
            'total_items': paginator.page.paginator.count,
            'next_page': paginator.get_next_link(),
            'previous_page': paginator.get_previous_link(),
        }
        if result_page is not None: 
            return Response(context)
        return Response({'success':True,'products':serializer.data})    

@api_view(['GET', 'POST','DELETE','PATCH','UPDATE'])
def product_handler(request):
    time.sleep(1)
    if request.method == 'GET':
        if request.query_params.get('id') is not None:
            return product_detail_by_id(request)
        elif request.query_params.get('name') is not None:
            return product_detail_by_name(request)
        elif (request.query_params.get('category') is not None) or (request.query_params.get('title') is not None):
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
    if ('title' not in data):
        return Response({'success':False,'error':'Title is a mandatory field.'},status=status.HTTP_400_BAD_REQUEST)
    response=product_category_service.create_product_category(data)
    if(response['success']):
        return Response({'success':True,'data':response['data']},status=status.HTTP_201_CREATED)
    else:
        return Response({'success':False,'error':response['error']},status=status.HTTP_400_BAD_REQUEST)

def update_product_category(request):
    data=request.data
    if ('title' not in data):
        return Response({'success':False,'error':'Title is a mandatory field.'},status=status.HTTP_400_BAD_REQUEST)

    response=product_category_service.update_category(data)
    if(response['success']):
        return Response({'success':True,'data':response['data']},status=status.HTTP_200_OK)
    else:
        return Response({'success':False,'error':response['error']},status=status.HTTP_400_BAD_REQUEST)
    
def product_category_list(request):
    categories=product_category_service.list_product_categories()
    if(categories['success']==False):
        return Response({'success':False,'error':categories['error']},status=status.HTTP_400_BAD_REQUEST)
    categories=categories['data']
    paginator=ProductPagination()
    result_page=paginator.paginate_queryset(list(categories),request)
    serializer=ProductCategorySerializer(result_page if result_page is not None else categories,many=True)
    result=serializer.data
    # print(result)
    context = {
        'categories': serializer.data,
        'current_page': paginator.page.number,
        'total_pages': paginator.page.paginator.num_pages,
        'total_items': paginator.page.paginator.count,
        'next_page': paginator.get_next_link(),
        'previous_page': paginator.get_previous_link(),
    }
    if result_page is not None: 
        return Response({'success':True,'data':context})
    return Response({'success':True,'data':serializer.data})

def get_category_by_name(request):
    category_name=request.query_params.get('category')

    category=product_category_service.get_category_by_name(category_name)
    if "error" in category:
        return Response({'success':False,'error':category['error']}, status=status.HTTP_404_NOT_FOUND)
    elif category["success"]:
        return Response({'success':True,'data':category['data']}, status=status.HTTP_200_OK)
    else:
        return Response({'success':False,'error':category['error']}, status=status.HTTP_400_BAD_REQUEST)

def get_category_by_id(request):
    category_id=request.query_params.get('id')
    category=product_category_service.get_category_by_id(category_id)
    if "error" in category:
        return Response({'success':False,'error':category['error']}, status=status.HTTP_404_NOT_FOUND)
    elif category["success"]:
        return Response({'success':True,'data':category['data']}, status=status.HTTP_200_OK)
    else:
        return Response({'success':False,'error':category['error']}, status=status.HTTP_400_BAD_REQUEST)
    
def delete_product_category(request):
    category_title=request.query_params.get('category')
    response=product_category_service.delete_product_category(category_title)
    if(response['success']):
        return Response({'success':True,'data':response['data']},status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'success':False,'error':response['error']},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST','PATCH','UPDATE','DELETE'])
def category_handler(request):
    time.sleep(1)
    if request.method == 'GET':
        if (not request.query_params) or (request.query_params.get('page') is not None):
            return product_category_list(request)
        elif request.query_params.get('category') is not None:
            return get_category_by_name(request)
        elif request.query_params.get('id') is not None:
            return get_category_by_id(request)
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