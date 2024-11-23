from django.db import models

# Create your models here.
class Product(models.Model):

    class CategoryChoices(models.TextChoices):
        SPORTS = 'SPORTS', 'Sports'
        FOODS = 'FOODS', 'Foods'
        ACCESSORIES = 'ACCESSORIES', 'Accessories'
        CLOTHING = 'CLOTHING', 'Clothing'

    
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(
        max_length=20,
        choices=CategoryChoices.choices,
        default=CategoryChoices.SPORTS
    )
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def __str__(self):
        return self.name

