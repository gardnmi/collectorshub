# Assuming users can own/sell collectibles
from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=50, default='Uncategorized')
    
    def __str__(self):
        return self.display_name
    
    class Meta:
        verbose_name_plural = "Categories"


class Collectible(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='collectibles')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField(Category, related_name='collectibles')
    condition = models.CharField(
        max_length=50,
        choices=[
            ('new', 'New'),
            ('used_like_new', 'Used - Like New'),
            ('used_good', 'Used - Good'),
            ('used_fair', 'Used - Fair'),
            ('for_parts', 'For Parts or Not Working'),
        ],
        default='used_good'
    )
    image = models.ImageField(
        upload_to='collectibles_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated_at']
