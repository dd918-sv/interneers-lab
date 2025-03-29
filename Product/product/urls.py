from django.urls import re_path
from . import views

urlpatterns=[ 
    re_path(r'^products/?$',views.product_list,name='product_list'),
    re_path(r'^products/detail_id/?$',views.product_detail_by_id),
    re_path(r'^products/detail_name/?$',views.product_detail_by_name),
    re_path(r'^products/create/?$',views.create_product),
    re_path(r'^products/update/?$',views.update_product),
    re_path(r'^products/delete/?$',views.delete_product),
    re_path(r'^',views.home)
]