from django.db import models
from django.contrib.auth.models import User
from shop.models import Product
from users.models import CustomUser

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField( max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Payment(models.Model):
    PAYMENT_STATUS = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    card_number = models.CharField(max_length=20, null=True, blank=True)
    expiry_date = models.CharField(max_length=5,  null=True, blank=True)
    cvv = models.CharField(max_length=4, null=True, blank=True)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'Payment {self.payment_id} by {self.user}'