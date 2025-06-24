from django.contrib import admin
from .models import Product
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('name', 'category', 'price', 'size', 'stock', 'created_at')
    list_filter = ('category', 'size')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name', )}