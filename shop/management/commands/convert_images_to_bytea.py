import mimetypes
import os
from django.core.management.base import BaseCommand
from shop.models import Product

class Command(BaseCommand):
    help = 'Convert product images to BYTEA and update the database'

    def handle(self, *args, **kwargs):
        # Base directory where images are stored
        base_dir = 'shop/product_images/'  # Adjust this path as needed

        # Get all products
        products = Product.objects.all()

        for product in products:
            if product.image:  # Check if the product has an image field with a valid path
                image_path = os.path.join(base_dir, str(product.image))

                try:
                    # Read the image as binary data
                    with open(image_path, 'rb') as img_file:
                        binary_data = img_file.read()

                    # Guess the MIME type of the image
                    mime_type, _ = mimetypes.guess_type(image_path)

                    # Update the product record with the binary data and MIME type
                    product.image = binary_data
                    product.image_mime_type = mime_type or 'application/octet-stream'  # Fallback MIME type
                    product.save()

                    self.stdout.write(self.style.SUCCESS(f"Successfully updated: {product.name}"))

                except FileNotFoundError:
                    self.stdout.write(self.style.WARNING(f"Image not found for: {product.name} at {image_path}"))

        self.stdout.write(self.style.SUCCESS('Image conversion completed.'))
