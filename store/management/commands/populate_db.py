from django.core.management.base import BaseCommand
from store.models import Category, Product, Size
from django.core.files import File
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Populate database with sample products'

    def handle(self, *args, **kwargs):
        # Create categories
        categories = [
            {'name': 'Running', 'description': 'High-performance running shoes'},
            {'name': 'Casual', 'description': 'Comfortable everyday shoes'},
            {'name': 'Sport', 'description': 'Athletic and training shoes'},
            {'name': 'Fashion', 'description': 'Trendy and stylish shoes'},
        ]

        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Sample products data
        products = [
            {
                'name': 'PandaSpeed Runner',
                'description': 'Lightweight running shoes with superior cushioning',
                'price': 129.99,
                'category': 'Running',
                'brand': 'PandaShoes',
                'sku': 'PS-RUN-001',
                'sizes': [
                    {'size': '40', 'gender': 'M', 'quantity': 10},
                    {'size': '41', 'gender': 'M', 'quantity': 15},
                    {'size': '42', 'gender': 'M', 'quantity': 20},
                ]
            },
            {
                'name': 'Urban Panda Casual',
                'description': 'Stylish and comfortable casual shoes',
                'price': 89.99,
                'category': 'Casual',
                'brand': 'PandaShoes',
                'sku': 'PS-CAS-001',
                'sizes': [
                    {'size': '39', 'gender': 'U', 'quantity': 12},
                    {'size': '40', 'gender': 'U', 'quantity': 18},
                    {'size': '41', 'gender': 'U', 'quantity': 15},
                ]
            },
            {
                'name': 'PandaFlex Training',
                'description': 'Versatile training shoes for gym and sports',
                'price': 109.99,
                'category': 'Sport',
                'brand': 'PandaShoes',
                'sku': 'PS-SPT-001',
                'sizes': [
                    {'size': '40', 'gender': 'M', 'quantity': 8},
                    {'size': '41', 'gender': 'M', 'quantity': 12},
                    {'size': '42', 'gender': 'M', 'quantity': 10},
                ]
            },
            {
                'name': 'Panda Fashion Elite',
                'description': 'Premium fashion sneakers for the style-conscious',
                'price': 149.99,
                'category': 'Fashion',
                'brand': 'PandaShoes',
                'sku': 'PS-FSH-001',
                'sizes': [
                    {'size': '38', 'gender': 'W', 'quantity': 15},
                    {'size': '39', 'gender': 'W', 'quantity': 20},
                    {'size': '40', 'gender': 'W', 'quantity': 18},
                ]
            },
            {
                'name': 'PandaAir Boost',
                'description': 'Advanced cushioning technology for long-distance running',
                'price': 159.99,
                'category': 'Running',
                'brand': 'PandaShoes',
                'sku': 'PS-RUN-002',
                'sizes': [
                    {'size': '41', 'gender': 'U', 'quantity': 10},
                    {'size': '42', 'gender': 'U', 'quantity': 15},
                    {'size': '43', 'gender': 'U', 'quantity': 12},
                ]
            },
        ]

        for product_data in products:
            category = Category.objects.get(name=product_data['category'])
            product, created = Product.objects.get_or_create(
                sku=product_data['sku'],
                defaults={
                    'name': product_data['name'],
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'category': category,
                    'brand': product_data['brand'],
                }
            )

            if created:
                self.stdout.write(f'Created product: {product.name}')
                # Create sizes for the product
                for size_data in product_data['sizes']:
                    Size.objects.create(
                        product=product,
                        size=size_data['size'],
                        gender=size_data['gender'],
                        quantity=size_data['quantity']
                    )
                self.stdout.write(f'Added sizes for: {product.name}')

        self.stdout.write(self.style.SUCCESS('Successfully populated database'))
