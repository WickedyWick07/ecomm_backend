from django.urls import path
from . import views 
from django.urls import re_path
from django.conf import settings 
from django.views.static import serve

urlpatterns = [
    path('products/', views.product_list, name='product-list'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('products/create/', views.product_create, name='product-create'),
    path('products/<int:pk>/update/', views.product_update, name='product-update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product-delete'),
    path('products/<int:pk>/update_stock/', views.update_stock, name='product-update-stock'),
    re_path(r'^media/(?P<path>.*)$', views.serve_media, name='serve_media')
]

if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

