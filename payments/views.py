# views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
import paypalrestsdk
from .models import Order, OrderItem, Payment
from .serializers import OrderSerializer 
from cart.models import Cart
from django.db import transaction
import uuid

paypalrestsdk.configure({
    "mode": "sandbox", # Change to "live" when you're ready to go live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_payment(request):
    print('Payment received')

    payment_method = request.data.get('payment_method')
    card_details = request.data.get('cardDetails', {})
    amount = request.data.get('amount')

    if payment_method == 'card':

        payment_id = str(uuid.uuid4())
        payment = Payment.objects.create(
            user=request.user,
            payment_id=payment_id,
            amount=amount,
            payment_method='card',
            card_number=card_details.get('cardNumber'),
            expiry_date=card_details.get('expiryDate'),
            cvv=card_details.get('cvv'),
            status='Paid'
        )
            
        

        try:
            # Retrieve the cart
            cart = Cart.objects.get(user=request.user)

            # Create the order
            order = Order.objects.create(
                user=request.user,
                total_amount=amount,
                payment_id=payment_id,
                status='Paid'
            )

            # Create order items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )

            # Clear the cart
            cart.items.all().delete()

            serializer = OrderSerializer(order)
            return Response({
                "message": "Payment processed successfully",
                "order": serializer.data
            }, status=200)
        except Exception as e:
            # Handle the exception by deleting the payment and returning an error response
            payment.delete()
            return Response({"error": str(e)}, status=500)
    
    
    elif payment_method == 'paypal':
        payment_id = request.data.get('paymentID')
        payer_id = request.data.get('payerID')

        if not (payment_id and payer_id):
            return Response({"error": "Payment ID and Payer ID are required"}, status=400)

        try:
            payment = paypalrestsdk.Payment.find(payment_id)
            if payment.execute({'payer_id': payer_id}):
                with transaction.atomic():
                    cart = Cart.objects.get(user=request.user)
                    order = Order.objects.create(
                        user=request.user, 
                        total_amount=payment.transactions[0].amount.total,
                        payment_id=payment_id,
                        status='Paid'
                    )

                    for cart_item in cart.items.all():
                        OrderItem.objects.create(
                            order=order,
                            product=cart_item.product,
                            quantity=cart_item.quantity,
                            price=cart_item.product.price
                        )

                    cart.items.all().delete()

                    serializer = OrderSerializer(order)

                    return Response({
                        "message": "PayPal payment processed successfully",
                        "order": serializer.data
                    }, status=200)
            else:
                return Response({"error": "Payment not found"}, status=404)

        except paypalrestsdk.ResourceNotFound:
            return Response({"error": "PayPal payment not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    else:
        return Response({"error": "Invalid payment method"}, status=400)
