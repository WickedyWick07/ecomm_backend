from django.urls import path 
from . import views 

urlpatterns = [
    path("cart/", views.cart_detail, name='view_cart'),
    path("cart/total_price/", views.cart_total_price, name='total_price'),
    path("cart/add/", views.add_to_cart, name='add_cart'),
    path('cart/update/<int:item_id>/', views.cart_update_item, name='update_cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_cart'),
]
