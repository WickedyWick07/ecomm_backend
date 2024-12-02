from django.urls import path
from . import views 

urlpatterns = [
    path('products/', views.product_list, name='product-list'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('products/create/', views.product_create, name='product-create'),
    path('products/<int:pk>/update/', views.product_update, name='product-update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product-delete'),
    path('products/<int:pk>/update_stock/', views.update_stock, name='product-update-stock'),
    path('product-image/<int:pk>/', views.serve_product_image, name='product_image'),

]
