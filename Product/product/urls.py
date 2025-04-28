from django.urls import re_path
from . import views

urlpatterns=[ 
    re_path(r'^products/',views.product_handler),
    re_path(r'^category/?$',views.category_handler),
    re_path(r'^',views.home)
]