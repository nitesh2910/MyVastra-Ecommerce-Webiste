from django.db import models
from category.models import Category

# Create your models here.
class Product(models.Model):
    SIZE_CHOICES = [
        ('FS', 'Free Size'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES, default='FS')
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name