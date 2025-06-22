from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from a_collectibles.models import Collectible, Category
import random

def ensure_default_categories():
    default_categories = [
        {"name": "antiques", "display_name": "Antiques"},
        {"name": "books", "display_name": "Books"},
        {"name": "electronics", "display_name": "Electronics"},
        {"name": "furniture", "display_name": "Furniture"},
        {"name": "clothing", "display_name": "Clothing"},
        {"name": "toys", "display_name": "Toys"},
        {"name": "art", "display_name": "Art"},
        {"name": "sports", "display_name": "Sports Equipment"},
        {"name": "tools", "display_name": "Tools"},
        {"name": "miscellaneous", "display_name": "Miscellaneous"},
    ]
    for category in default_categories:
        Category.objects.get_or_create(
            name=category["name"], defaults={"display_name": category["display_name"]}
        )

class Command(BaseCommand):
    help = "Generate 120+ sample collectibles for testing."

    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR("No users found. Please create a user first."))
            return

        ensure_default_categories()
        categories = list(Category.objects.all())
        if not categories:
            self.stdout.write(self.style.ERROR("No categories found. Please run migrations and ensure categories exist."))
            return

        names = [
            "Vintage Clock", "Rare Comic Book", "Antique Vase", "Signed Baseball", "Classic Novel",
            "Retro Game Console", "Limited Edition Sneakers", "Collectible Card", "Old Coin", "Art Print",
            "Model Train", "Action Figure", "Porcelain Doll", "Historic Map", "Autographed Poster",
            "First Edition Book", "Rare Stamp", "Ceramic Plate", "Sports Jersey", "Movie Prop",
            "Board Game", "Vinyl Record", "Handmade Quilt", "Crystal Figurine", "Bronze Statue",
            "Miniature Car", "Fossil", "Gemstone", "Vintage Camera", "Old Photograph",
        ]
        conditions = ["new", "used_like_new", "used_good", "used_fair", "for_parts"]
        base_desc = "This is a sample collectible for testing the CollectorsHub platform."

        count = 120
        created = 0
        for i in range(count):
            name = random.choice(names) + f" #{i+1}"
            description = base_desc + f" (Sample #{i+1})"
            price = round(random.uniform(10, 500), 2)
            condition = random.choice(conditions)
            collectible = Collectible.objects.create(
                owner=user,
                name=name,
                description=description,
                price=price,
                condition=condition,
            )
            # Assign 1-3 random categories
            collectible.categories.set(random.sample(categories, k=random.randint(1, 3)))
            created += 1
        self.stdout.write(self.style.SUCCESS(f"Created {created} sample collectibles for user {user.username}."))
