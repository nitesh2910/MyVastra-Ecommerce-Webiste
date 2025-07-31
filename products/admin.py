from django.contrib import admin
from .models import Product
from category.models import Category
from django.utils.text import slugify


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'size', 'stock', 'created_at')
    list_filter = ('category', 'size')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.name)
        super().save_model(request, obj, form, change)
