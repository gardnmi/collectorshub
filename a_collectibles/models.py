# Assuming users can own/sell collectibles
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=50, default="Uncategorized")

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name_plural = "Categories"


class Collectible(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="collectibles"
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField(Category, related_name="collectibles")
    condition = models.CharField(
        max_length=50,
        choices=[
            ("new", "New"),
            ("used_like_new", "Used - Like New"),
            ("used_good", "Used - Good"),
            ("used_fair", "Used - Fair"),
            ("for_parts", "For Parts or Not Working"),
        ],
        default="used_good",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def primary_image(self):
        return self.images.filter(is_primary=True).first() or self.images.first() # type: ignore

    class Meta:
        ordering = ["-updated_at"]


class CollectibleImage(models.Model):
    collectible = models.ForeignKey(
        Collectible, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="collectibles_images/")
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Image for {self.collectible.name} ({'Primary' if self.is_primary else 'Secondary'})"

    class Meta:
        ordering = ["-is_primary", "uploaded_at"]