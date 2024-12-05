from rest_framework import permissions, filters
from rest_framework.decorators import api_view, permission_classes, action 
from rest_framework.response import Response 
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from ecomm_backend.pagination import CustomPageNumberPagination
from .serializers import ProductSerializer
import binascii
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404
from django.views.decorators.http import require_GET
import os
import mimetypes
from django.conf import settings

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def serve_media(request, path):
    try:
        # Construct the full path to the media file
        media_root = settings.MEDIA_ROOT
        file_path = os.path.join(media_root, path)
        
        # Verify file exists
        if not os.path.exists(file_path):
            raise Http404("File not found")
        
        # Determine MIME type based on file extension
        content_type, _ = mimetypes.guess_type(file_path)
        
        # Fallback to specific image MIME types if guess fails
        if not content_type:
            if file_path.lower().endswith('.jpg') or file_path.lower().endswith('.jpeg'):
                content_type = 'image/jpeg'
            elif file_path.lower().endswith('.png'):
                content_type = 'image/png'
            elif file_path.lower().endswith('.gif'):
                content_type = 'image/gif'
            else:
                content_type = 'application/octet-stream'
        
        # Open and serve the file
        response = FileResponse(
            open(file_path, 'rb'), 
            content_type=content_type
        )
        
        # Add caching headers
        response['Cache-Control'] = 'public, max-age=86400'  # Cache for 24 hours
        
        return response
    
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Error serving media file: {e}")
        raise Http404("Error serving file")

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def product_create(request):
    queryset = Product.objects.all()
    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.error, status=400)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def product_list(request):
    queryset = Product.objects.all().order_by('id')
    serializer = ProductSerializer(data=request.data)
    

    min_price = request.query_params.get("min_price")  
    max_price = request.query_params.get("max_price")
    if min_price:
        queryset = queryset.filter(price_gte=min_price)

    if max_price:
        queryset = queryset.filter(price_lte=max_price)

    search = request.query_params.get("search")
    if search: 
        queryset = queryset.filter(name__icontains=search) | queryset.filter(category__icontains=search)
        

    ordering = request.query_params.get('ordering')
    if ordering:
        queryset = queryset.order_by(ordering)

    paginator = CustomPageNumberPagination()
    paginated_queryset = paginator.paginate_queryset(queryset, request)

    serializer = ProductSerializer(paginated_queryset, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=404)
    
    serializer = ProductSerializer(product)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def product_update(request, pk):
    try: 
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=404)
    
    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def product_delete(request, pk):
    try: 
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=404)
    
    product.delete()
    return Response(status=204)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_stock(request, pk):
    try: 
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=404)


    quantity = int(request.data.get('quantity', 0))
    if product.stock >= quantity:
        product.stock -= quantity
        product.save()
        return Response({'status': 'stock updated'})
    else: 
        return Response({"status": 'not enough stock'}, status=400)