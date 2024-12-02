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

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def serve_product_image(request, pk):
    try:
        # Fetch the product with the given ID
        product = get_object_or_404(Product, pk=pk)

        # Ensure the product has an image
        if product.image:
            # Convert the hex-encoded image data to raw bytes
            image_data = binascii.unhexlify(product.image.hex().replace('\\x', ''))

            # Determine the appropriate content type (e.g., 'image/jpeg', 'image/png')
            content_type = 'image/jpeg'  # Adjust based on your image type

            # Serve the image as an HTTP response
            return HttpResponse(image_data, content_type=content_type)

        else:
            return HttpResponse('No image found for this product', status=404)

    except Product.DoesNotExist:
        return HttpResponse('Product not found', status=404)

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
    queryset = Product.objects.all()
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