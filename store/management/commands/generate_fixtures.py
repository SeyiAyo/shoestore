from django.core.management.base import BaseCommand
import json
import random
from datetime import datetime, timezone

class Command(BaseCommand):
    help = 'Generate fixture data for the store'

    def handle(self, *args, **kwargs):
        current_time = datetime.now(timezone.utc).isoformat()

        # Categories
        categories = [
            {"model": "store.category", "pk": 1, "fields": {"name": "Running", "description": "High-performance running shoes", "created_at": current_time}},
            {"model": "store.category", "pk": 2, "fields": {"name": "Basketball", "description": "Professional basketball shoes", "created_at": current_time}},
            {"model": "store.category", "pk": 3, "fields": {"name": "Casual", "description": "Everyday comfort sneakers", "created_at": current_time}},
            {"model": "store.category", "pk": 4, "fields": {"name": "Training", "description": "Cross-training and gym shoes", "created_at": current_time}},
            {"model": "store.category", "pk": 5, "fields": {"name": "Soccer", "description": "Professional soccer cleats", "created_at": current_time}},
            {"model": "store.category", "pk": 6, "fields": {"name": "Tennis", "description": "Court performance shoes", "created_at": current_time}},
            {"model": "store.category", "pk": 7, "fields": {"name": "Skateboarding", "description": "Durable skate shoes", "created_at": current_time}}
        ]

        # Product name components
        prefixes = ["Air", "Ultra", "Pro", "Elite", "Zoom", "Boost", "Fresh", "Power", "Speed", "Max"]
        models = ["Runner", "Trainer", "Force", "Classic", "Lite", "Sport", "Flow", "Glide", "Dash", "Swift"]
        numbers = ["1.0", "2.0", "3.0", "4.0", "5.0", "X", "GT", "Plus", "Premium", "Limited"]

        # Product descriptions
        desc_templates = [
            "Experience ultimate comfort and style with these {category} shoes. Features advanced {tech} technology.",
            "Professional-grade {category} footwear with {tech} cushioning for maximum performance.",
            "Elevate your game with these premium {tech}-enhanced {category} shoes.",
            "Designed for both style and performance, these {category} shoes incorporate cutting-edge {tech} technology.",
            "Premium {category} shoes with innovative {tech} system for superior comfort and durability."
        ]

        technologies = [
            "air cushioning", "responsive foam", "energy return", "breathable mesh", 
            "carbon fiber plate", "dynamic support", "adaptive fit", "reactive cushioning",
            "stability control", "impact protection"
        ]

        # Generate 100 products
        products = []
        for i in range(1, 101):
            category = random.choice(categories)
            name = f"{random.choice(prefixes)} {random.choice(models)} {random.choice(numbers)}"
            description = random.choice(desc_templates).format(
                category=category['fields']['name'].lower(),
                tech=random.choice(technologies)
            )
            
            price = round(random.uniform(59.99, 299.99), 2)
            stock = random.randint(10, 100)
            rating = round(random.uniform(3.5, 5.0), 2)
            review_count = random.randint(5, 500)

            product = {
                "model": "store.product",
                "pk": i,
                "fields": {
                    "name": name,
                    "description": description,
                    "price": str(price),
                    "stock": stock,
                    "rating": str(rating),
                    "review_count": review_count,
                    "created_at": current_time,
                    "image": None
                }
            }
            products.append(product)

            # Generate sizes for each product
            sizes = []
            size_pk = (i - 1) * 15 + 1  # Unique size PKs for each product
            for us_size in range(7, 15):  # US sizes 7-14
                for gender in ['M', 'W']:
                    sizes.append({
                        "model": "store.size",
                        "pk": size_pk,
                        "fields": {
                            "product": i,
                            "size": f"US {us_size}",
                            "gender": gender,
                            "quantity": random.randint(0, 20)
                        }
                    })
                    size_pk += 1

            products.extend(sizes)

        # Combine all fixtures
        fixtures = categories + products

        # Write to file
        with open('store/fixtures/initial_data.json', 'w') as f:
            json.dump(fixtures, f, indent=4)

        self.stdout.write(self.style.SUCCESS('Successfully generated fixture data'))
