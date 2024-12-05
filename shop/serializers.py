from rest_framework import serializers
from .models import Product
from django.conf import settings

class ProductSerializer(serializers.ModelSerializer):
    # Adding a custom field to return the full image URL
    image_url = serializers.SerializerMethodField()
    ordering = ['id']  # Replace 'id' with the desired field


    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'stock', 'image', 'image_url']

    def get_image_url(self, obj):
        # Check if the product has an image
        if obj.image:
            # Replace the 'media/' prefix with the Netlify URL
            return f"{settings.NETLIFY_MEDIA_URL}{obj.image.name.replace('/media/', '')}"
        return None
