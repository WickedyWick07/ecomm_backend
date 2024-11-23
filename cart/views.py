from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated 
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from shop.models import Product

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id= request.data.get("product_id")
    quantity = int(request.data.get('quantity', 1))

    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created: 
        cart_item.quantity += quantity
        cart_item.save()

    serializer = CartItemSerializer(cart_item)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, pk):
    try:
        cart_item = CartItem.objects.get(pk=pk, cart__user=request.user)
        cart_item.delete()
        return Response({'message': 'item removed from cart successfully.'})
    except CartItem.DoesNotExist:
        return Response({'error': "Item not found"}, status=404)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_total_price(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return Response({'total_price': total_price})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def cart_update_item(request, item_id):
    new_quantity = request.data.get('quantity')
    try:
        item = CartItem.objects.get(id=item_id, cart__user=request.user)
        item.quantity = new_quantity
        item.save()
        return Response({'message': 'Quantity updated successfully'}, status=200)
    except CartItem.DoesNotExist:
        return Response({'error': 'Item not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)