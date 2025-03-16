from django.urls import path
from . import views

urlpatterns=[
    path('',views.home),
    path('products/',views.product_list),
    path('products/<int:id>/',views.product_detail),
    path('products/create/',views.create_product),
    path('products/update/',views.update_product),
    path('products/delete/',views.delete_product)
]