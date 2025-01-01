from django.core.management.base import BaseCommand
from store.models import Category, Product, Size
import random
from decimal import Decimal
import uuid

class Command(BaseCommand):
    help = 'Populate database with sneakers'

    def handle(self, *args, **kwargs):
        # Create categories if they don't exist
        categories = {
            'Running': 'Athletic shoes designed for running and jogging',
            'Basketball': 'High-performance shoes for basketball players',
            'Casual': 'Comfortable shoes for everyday wear',
            'Training': 'Versatile shoes for various workout activities',
            'Lifestyle': 'Fashion-forward sneakers for street style',
            'Tennis': 'Specialized shoes for tennis and court sports',
            'Skateboarding': 'Durable shoes designed for skateboarding',
            'Walking': 'Comfortable shoes optimized for walking'
        }

        for name, desc in categories.items():
            Category.objects.get_or_create(name=name, description=desc)

        # Sneaker brands
        brands = ['Nike', 'Adidas', 'Puma', 'New Balance', 'Reebok', 'Under Armour', 
                 'ASICS', 'Converse', 'Vans', 'Jordan']

        # Unsplash sneaker image URLs
        unsplash_urls = [
            'https://images.unsplash.com/photo-1542291026-7eec264c27ff',
            'https://images.unsplash.com/photo-1608231387042-66d1773070a5',
            'https://images.unsplash.com/photo-1607853202273-797f1c22a38e',
            'https://images.unsplash.com/photo-1579338559194-a162d19bf842',
            'https://images.unsplash.com/photo-1549298916-b41d501d3772',
            'https://images.unsplash.com/photo-1600185365926-3a2ce3cdb9eb',
            'https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a',
            'https://images.unsplash.com/photo-1587563871167-1ee9c731aefb',
            'https://images.unsplash.com/photo-1605348532760-6753d2c43329',
            'https://images.unsplash.com/photo-1460353581641-37baddab0fa2',
            'https://images.unsplash.com/photo-1512374382149-233c42b6a83b',
            'https://images.unsplash.com/photo-1491553895911-0055eca6402d',
            'https://images.unsplash.com/photo-1542674093-59dc69e47b4f',
            'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa',
            'https://images.unsplash.com/photo-1560769629-975ec94e6a86',
            'https://images.unsplash.com/photo-1515955656352-a1fa3ffcd111',
            'https://images.unsplash.com/photo-1539185441755-769473a23570',
            'https://images.unsplash.com/photo-1520256862855-398228c41684',
            'https://images.unsplash.com/photo-1552346154-21d32810aba3',
            'https://images.unsplash.com/photo-1518002171953-a080ee817e1f'
        ]

        # Shoe names and descriptions
        shoe_types = ['Pro', 'Elite', 'Boost', 'Air', 'Classic', 'Ultra', 'Max', 'Zoom', 
                     'Flow', 'Lite', 'Plus', 'Cloud', 'Flex', 'Free', 'Rush', 'Swift', 
                     'Rapid', 'Glide', 'Wave', 'Force']
        
        descriptors = ['Performance', 'Premium', 'Limited Edition', 'Signature', 'Essential',
                      'Advanced', 'Professional', 'Sport', 'Core', 'Next Gen']

        # Create 200 sneakers
        for i in range(200):
            brand = random.choice(brands)
            category = Category.objects.order_by('?').first()
            shoe_type = random.choice(shoe_types)
            descriptor = random.choice(descriptors)
            
            name = f"{brand} {descriptor} {shoe_type} {random.randint(1, 9)}"
            description = f"The {name} delivers unmatched comfort and style. " \
                         f"Perfect for {category.name.lower()} enthusiasts who demand " \
                         f"both performance and aesthetics."
            
            price = Decimal(random.randint(7999, 24999)) / 100  # Random price between 79.99 and 249.99
            rating = round(random.uniform(3.5, 5.0), 1)
            review_count = random.randint(10, 1000)
            
            # Generate unique SKU
            sku = f"{brand[:3].upper()}{category.name[:3].upper()}{str(uuid.uuid4())[:8]}"
            
            # Create product
            product = Product.objects.create(
                name=name,
                description=description,
                price=price,
                category=category,
                brand=brand,
                rating=rating,
                review_count=review_count,
                image=random.choice(unsplash_urls),
                sku=sku
            )

            # Add sizes
            sizes = ['US 6', 'US 7', 'US 8', 'US 9', 'US 10', 'US 11', 'US 12']
            for size in sizes:
                Size.objects.create(
                    product=product,
                    size=size,
                    gender='U',  # Unisex
                    quantity=random.randint(0, 50)  # Random stock quantity
                )

            self.stdout.write(f'Created product: {name}')
